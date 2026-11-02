document.addEventListener('DOMContentLoaded', async () => {
    let supabase;
    try {
        const supabaseUrl = 'https://qokgtrabcxtxlympbkyb.supabase.co';
        const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME';
        if (window.supabase) {
            supabase = window.supabase.createClient(supabaseUrl, supabaseKey);
        }
    } catch (e) {
        console.error("Supabase init error:", e);
        return;
    }

    if (!supabase) {
        alert("Database connection not ready.");
        return;
    }

    // ── Security constants ─────────────────────────────────────────────────────
    const MAX_GUESTS   = 20;   // VULN-015 FIX
    const MAX_SESSIONS = 30;   // VULN-015 FIX
    const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];  // VULN-004
    const MAX_IMAGE_MB = 4;    // VULN-004 FIX
    const MAX_TITLE_LEN = 150; // VULN-003 FIX
    const MAX_DESC_LEN  = 2000;

    // VULN-004 FIX: Validate image files before upload
    function validateImageFile(file) {
        if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
            throw new Error('Only JPEG, PNG, WebP, and GIF images are allowed.');
        }
        if (file.size > MAX_IMAGE_MB * 1024 * 1024) {
            throw new Error(`Image must be under ${MAX_IMAGE_MB}MB.`);
        }
    }

    // VULN-017 FIX: GPS coordinate range validation
    function validateGPS(lat, lng, radius) {
        const latN = parseFloat(lat), lngN = parseFloat(lng), radN = parseInt(radius, 10);
        if (isNaN(latN) || latN < -90  || latN > 90)    throw new Error('Latitude must be between -90 and 90.');
        if (isNaN(lngN) || lngN < -180 || lngN > 180)   throw new Error('Longitude must be between -180 and 180.');
        if (isNaN(radN) || radN < 10   || radN > 10000) throw new Error('Radius must be between 10m and 10,000m.');
        return { lat: latN, lng: lngN, radius: radN };
    }

    let organizerId = null;

    // Check Auth
    try {
        const { data: { session }, error: sessionError } = await supabase.auth.getSession();
        if (sessionError || !session) {
            window.location.href = 'login.html';
            return;
        }
        
        // VULN-013 FIX: Fetch only needed columns — no secret_key sent to client
        const { data: profile } = await supabase.from('profiles')
            .select('id, full_name, role')
            .eq('id', session.user.id).single();
        if (profile) {
            organizerId = profile.id;
            const initials = profile.full_name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            document.getElementById('profile-avatar').textContent = initials;
        } else {
            window.location.href = 'login.html';
            return;
        }
    } catch (e) {
        if (location.hostname === 'localhost') console.error('[DEBUG]', e);
    }

    // Image Preview Logic
    const bannerInput = document.getElementById('banner-input');
    const bannerPreview = document.getElementById('banner-preview');
    const uploadPlaceholder = document.getElementById('uploadPlaceholder');
    let selectedFile = null;

    bannerInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            selectedFile = file;
            const reader = new FileReader();
            reader.onload = (e) => {
                bannerPreview.src = e.target.result;
                bannerPreview.style.display = 'block';
                uploadPlaceholder.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    });

    // Store global event data
    const eventDraft = {};

    // Step 1 Submission
    document.getElementById('btnContinueStep1').addEventListener('click', async (e) => {
        const btnContinue = document.getElementById('btnContinueStep1');
        btnContinue.textContent = 'Saving...';
        btnContinue.disabled = true;

        const title = document.getElementById('eventName').value;
        const description = document.getElementById('eventDescription').value;
        const category = document.getElementById('eventCategory').value;

        // VULN-003 FIX: Enforce input length limits
        if (!title || title.trim().length === 0) {
            alert('Event name is required');
            btnContinue.textContent = 'Continue →';
            btnContinue.disabled = false;
            return;
        }
        if (title.length > MAX_TITLE_LEN) {
            alert(`Event name must be under ${MAX_TITLE_LEN} characters.`);
            btnContinue.textContent = 'Continue →';
            btnContinue.disabled = false;
            return;
        }
        if (description.length > MAX_DESC_LEN) {
            alert(`Description must be under ${MAX_DESC_LEN} characters.`);
            btnContinue.textContent = 'Continue →';
            btnContinue.disabled = false;
            return;
        }

        try {
            let bannerUrl = null;

            // Upload image if selected
            if (selectedFile) {
                // VULN-004 FIX: Validate file type and size before upload
                try { validateImageFile(selectedFile); } catch (fileErr) {
                    alert(fileErr.message);
                    btnContinue.textContent = 'Continue →';
                    btnContinue.disabled = false;
                    return;
                }
                const fileExt = selectedFile.name.split('.').pop().toLowerCase();
                // VULN-016 FIX: Use crypto.randomUUID() instead of Math.random()
                const fileName = `${crypto.randomUUID()}.${fileExt}`;
                const filePath = `${organizerId}/${fileName}`;
                
                const { error: uploadError } = await supabase.storage
                    .from('event_banners')
                    .upload(filePath, selectedFile);
                    
                if (uploadError) throw uploadError;
                
                const { data: publicUrlData } = supabase.storage
                    .from('event_banners')
                    .getPublicUrl(filePath);
                    
                bannerUrl = publicUrlData.publicUrl;
            }

            // Save to draft memory
            eventDraft.title = title;
            eventDraft.description = description;
            eventDraft.category = category;
            eventDraft.banner_image_url = bannerUrl;

            // Transition to Step 2
            document.getElementById('step1-card').style.display = 'none';
            document.getElementById('step2-card').style.display = 'block';
            
            const step1 = document.getElementById('stepper-1');
            step1.classList.remove('active');
            step1.querySelector('.step-circle').innerHTML = '✓';
            step1.querySelector('.step-circle').style.backgroundColor = '#00b050';
            step1.querySelector('.step-circle').style.color = 'white';
            
            const step2 = document.getElementById('stepper-2');
            step2.classList.remove('inactive');
            step2.classList.add('active');

            btnContinue.textContent = 'Continue →';
            btnContinue.disabled = false;

        } catch (error) {
            console.error("Error saving step 1:", error);
            alert("Error: " + error.message);
            btnContinue.textContent = 'Continue →';
            btnContinue.disabled = false;
        }
    });

    // Step 2 Logic
    document.getElementById('btnBackStep2').addEventListener('click', () => {
        document.getElementById('step2-card').style.display = 'none';
        document.getElementById('step1-card').style.display = 'block';
        
        const step1 = document.getElementById('stepper-1');
        step1.classList.add('active');
        step1.querySelector('.step-circle').innerHTML = '1';
        step1.querySelector('.step-circle').style.backgroundColor = '';
        
        const step2 = document.getElementById('stepper-2');
        step2.classList.remove('active');
        step2.classList.add('inactive');
    });

    document.getElementById('btnContinueStep2').addEventListener('click', async () => {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        const startTime = document.getElementById('startTime').value;
        const endTime = document.getElementById('endTime').value;

        if (!startDate || !endDate || !startTime || !endTime) {
            alert('Please fill out all date and time fields.');
            return;
        }

        eventDraft.start_date = startDate;
        eventDraft.end_date = endDate;
        eventDraft.start_time = startTime;
        eventDraft.end_time = endTime;

        // Transition to Step 3
        document.getElementById('step2-card').style.display = 'none';
        document.getElementById('step3-card').style.display = 'block';
        
        const step2 = document.getElementById('stepper-2');
        step2.classList.remove('active');
        step2.querySelector('.step-circle').innerHTML = '✓';
        step2.querySelector('.step-circle').style.backgroundColor = '#00b050';
        step2.querySelector('.step-circle').style.color = 'white';
        
        const step3 = document.getElementById('stepper-3');
        step3.classList.remove('inactive');
        step3.classList.add('active');
    });

    // Step 3 Logic
    const updateGeofenceText = () => {
        const lat = document.getElementById('gpsLat').value || '13.0108';
        const lng = document.getElementById('gpsLng').value || '74.7943';
        const radius = document.getElementById('attendanceRadius').value || '100';
        document.getElementById('geofence-text').textContent = `${radius} m geofence · ${lat}, ${lng}`;
    };

    document.getElementById('gpsLat').addEventListener('input', updateGeofenceText);
    document.getElementById('gpsLng').addEventListener('input', updateGeofenceText);
    document.getElementById('attendanceRadius').addEventListener('input', updateGeofenceText);

    document.getElementById('btnBackStep3').addEventListener('click', () => {
        document.getElementById('step3-card').style.display = 'none';
        document.getElementById('step2-card').style.display = 'block';
        
        const step2 = document.getElementById('stepper-2');
        step2.classList.add('active');
        step2.querySelector('.step-circle').innerHTML = '2';
        step2.querySelector('.step-circle').style.backgroundColor = '';
        
        const step3 = document.getElementById('stepper-3');
        step3.classList.remove('active');
        step3.classList.add('inactive');
    });

    document.getElementById('btnContinueStep3').addEventListener('click', async () => {
        const venueName = document.getElementById('venueName').value;
        const address = document.getElementById('venueAddress').value;
        const lat = document.getElementById('gpsLat').value;
        const lng = document.getElementById('gpsLng').value;
        const radius = document.getElementById('attendanceRadius').value;

        if (!venueName || !lat || !lng || !radius) {
            alert('Please fill out all required location fields.');
            return;
        }

        // VULN-017 FIX: Validate GPS coordinates before accepting
        try {
            const gps = validateGPS(lat, lng, radius);
            eventDraft.latitude  = gps.lat;
            eventDraft.longitude = gps.lng;
            eventDraft.attendance_radius_meters = gps.radius;
        } catch (gpsErr) {
            alert(gpsErr.message);
            return;
        }

        // Transition to Step 4
        document.getElementById('step3-card').style.display = 'none';
        document.getElementById('step4-card').style.display = 'block';
        
        const step3 = document.getElementById('stepper-3');
        step3.classList.remove('active');
        step3.querySelector('.step-circle').innerHTML = '✓';
        step3.querySelector('.step-circle').style.backgroundColor = '#00b050';
        step3.querySelector('.step-circle').style.color = 'white';
        
        const step4 = document.getElementById('stepper-4');
        step4.classList.remove('inactive');
        step4.classList.add('active');
    });

    // Step 4 Logic
    const guestsContainer = document.getElementById('guests-container');
    let guestCount = 0;

    const addGuestCard = () => {
        guestCount++;
        const cardId = `guest-card-${guestCount}`;
        const cardHTML = `
            <div class="guest-card" id="${cardId}">
                <div class="form-group">
                    <label class="form-label">Guest name</label>
                    <input type="text" class="form-control guest-name" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Designation</label>
                    <input type="text" class="form-control guest-designation">
                </div>
                <div class="form-group">
                    <label class="form-label">Description</label>
                    <textarea class="form-control guest-description" style="min-height: 80px;"></textarea>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="position: relative;">
                        <button type="button" class="btn-upload-photo">Upload photo</button>
                        <input type="file" class="guest-photo-input" accept="image/*" style="position: absolute; top:0; left:0; width:100%; height:100%; opacity:0; cursor:pointer;">
                        <span class="photo-file-name" style="font-size: 12px; color: #4a5568; margin-left: 8px;"></span>
                    </div>
                    <button type="button" class="btn-remove-guest" onclick="document.getElementById('${cardId}').remove(); updateGuestRemoves();">
                        <span style="font-size: 16px;">🗑</span> Remove
                    </button>
                </div>
            </div>
        `;
        guestsContainer.insertAdjacentHTML('beforeend', cardHTML);
        
        // Handle photo display
        const newCard = document.getElementById(cardId);
        const fileInput = newCard.querySelector('.guest-photo-input');
        const fileNameSpan = newCard.querySelector('.photo-file-name');
        fileInput.addEventListener('change', (e) => {
            if (e.target.files[0]) {
                fileNameSpan.textContent = e.target.files[0].name;
            }
        });

        updateGuestRemoves();
    };

    const updateGuestRemoves = () => {
        const cards = document.querySelectorAll('.guest-card');
        cards.forEach(card => {
            const removeBtn = card.querySelector('.btn-remove-guest');
            // Hide remove button if there's only 1 card left
            if (cards.length === 1) {
                removeBtn.style.display = 'none';
            } else {
                removeBtn.style.display = 'flex';
            }
        });
    };

    document.getElementById('btnAddGuest').addEventListener('click', () => {
        // VULN-015 FIX: Cap maximum number of guests to prevent DoS
        if (document.querySelectorAll('.guest-card').length >= MAX_GUESTS) {
            alert(`Maximum ${MAX_GUESTS} guests allowed per event.`);
            return;
        }
        addGuestCard();
    });
    
    // Add first guest card by default
    addGuestCard();

    document.getElementById('btnBackStep4').addEventListener('click', () => {
        document.getElementById('step4-card').style.display = 'none';
        document.getElementById('step3-card').style.display = 'block';
        
        const step3 = document.getElementById('stepper-3');
        step3.classList.add('active');
        step3.querySelector('.step-circle').innerHTML = '3';
        step3.querySelector('.step-circle').style.backgroundColor = '';
        
        const step4 = document.getElementById('stepper-4');
        step4.classList.remove('active');
        step4.classList.add('inactive');
    });

    document.getElementById('btnContinueStep4').addEventListener('click', async () => {
        const btnContinue = document.getElementById('btnContinueStep4');
        btnContinue.textContent = 'Saving...';
        btnContinue.disabled = true;

        const guests = [];
        const guestCards = document.querySelectorAll('.guest-card');
        
        for (let card of guestCards) {
            const name = card.querySelector('.guest-name').value;
            const designation = card.querySelector('.guest-designation').value;
            const description = card.querySelector('.guest-description').value;
            const fileInput = card.querySelector('.guest-photo-input');
            let file = fileInput.files[0] ? fileInput.files[0] : null;

            if (name.trim() !== '') {
                guests.push({
                    name, designation, description, file
                });
            }
        }

        if (guests.length === 0) {
            alert('Please add at least one guest.');
            btnContinue.textContent = 'Continue →';
            btnContinue.disabled = false;
            return;
        }

        eventDraft.guests = guests;

        // Transition to Step 5
        document.getElementById('step4-card').style.display = 'none';
        document.getElementById('step5-card').style.display = 'block';
        
        const step4 = document.getElementById('stepper-4');
        step4.classList.remove('active');
        step4.querySelector('.step-circle').innerHTML = '✓';
        step4.querySelector('.step-circle').style.backgroundColor = '#00b050';
        step4.querySelector('.step-circle').style.color = 'white';
        
        const step5 = document.getElementById('stepper-5');
        step5.classList.remove('inactive');
        step5.classList.add('active');

        btnContinue.textContent = 'Continue →';
        btnContinue.disabled = false;
    });

    // Step 5 Logic
    const sessionsContainer = document.getElementById('sessions-container');
    let sessionCount = 0;

    const addSessionCard = () => {
        sessionCount++;
        const cardId = `session-card-${sessionCount}`;
        const cardHTML = `
            <div class="session-card" id="${cardId}">
                <div class="form-group">
                    <label class="form-label">Session name</label>
                    <input type="text" class="form-control session-name" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Speaker</label>
                    <input type="text" class="form-control session-speaker">
                </div>
                <div class="form-group">
                    <label class="form-label">Start time</label>
                    <input type="time" class="form-control session-start" value="09:15" required>
                </div>
                <div class="form-group">
                    <label class="form-label">End time</label>
                    <input type="time" class="form-control session-end" value="10:00" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Room</label>
                    <input type="text" class="form-control session-room">
                </div>
                <div style="display: flex; justify-content: flex-end;">
                    <button type="button" class="btn-remove-guest btn-remove-session" onclick="document.getElementById('${cardId}').remove(); updateSessionRemoves();">
                        <span style="font-size: 16px;">🗑</span> Remove
                    </button>
                </div>
            </div>
        `;
        sessionsContainer.insertAdjacentHTML('beforeend', cardHTML);
        updateSessionRemoves();
    };

    const updateSessionRemoves = () => {
        const cards = document.querySelectorAll('.session-card');
        cards.forEach(card => {
            const removeBtn = card.querySelector('.btn-remove-session');
            if (cards.length === 1) {
                removeBtn.style.display = 'none';
            } else {
                removeBtn.style.display = 'flex';
            }
        });
    };

    document.getElementById('btnAddSession').addEventListener('click', () => {
        // VULN-015 FIX: Cap maximum number of sessions to prevent DoS
        if (document.querySelectorAll('.session-card').length >= MAX_SESSIONS) {
            alert(`Maximum ${MAX_SESSIONS} sessions allowed per event.`);
            return;
        }
        addSessionCard();
    });
    addSessionCard();

    document.getElementById('btnBackStep5').addEventListener('click', () => {
        document.getElementById('step5-card').style.display = 'none';
        document.getElementById('step4-card').style.display = 'block';
        
        const step4 = document.getElementById('stepper-4');
        step4.classList.add('active');
        step4.querySelector('.step-circle').innerHTML = '4';
        step4.querySelector('.step-circle').style.backgroundColor = '';
        
        const step5 = document.getElementById('stepper-5');
        step5.classList.remove('active');
        step5.classList.add('inactive');
    });

    document.getElementById('btnContinueStep5').addEventListener('click', async () => {
        const btnContinue = document.getElementById('btnContinueStep5');
        btnContinue.textContent = 'Saving...';
        btnContinue.disabled = true;

        const sessions = [];
        const sessionCards = document.querySelectorAll('.session-card');
        
        for (let card of sessionCards) {
            const name = card.querySelector('.session-name').value;
            const speaker = card.querySelector('.session-speaker').value;
            const startTime = card.querySelector('.session-start').value;
            const endTime = card.querySelector('.session-end').value;
            const room = card.querySelector('.session-room').value;

            if (name.trim() !== '' && startTime !== '' && endTime !== '') {
                sessions.push({
                    name, speaker, start_time: startTime, end_time: endTime, room
                });
            }
        }

        if (sessions.length === 0) {
            alert('Please add at least one valid session.');
            btnContinue.textContent = 'Continue →';
            btnContinue.disabled = false;
            return;
        }

        eventDraft.sessions = sessions;

        // Transition to Step 6
        document.getElementById('step5-card').style.display = 'none';
        document.getElementById('step6-card').style.display = 'block';
        
        const step5 = document.getElementById('stepper-5');
        step5.classList.remove('active');
        step5.querySelector('.step-circle').innerHTML = '✓';
        step5.querySelector('.step-circle').style.backgroundColor = '#00b050';
        step5.querySelector('.step-circle').style.color = 'white';
        
        const step6 = document.getElementById('stepper-6');
        step6.classList.remove('inactive');
        step6.classList.add('active');

        btnContinue.textContent = 'Continue →';
        btnContinue.disabled = false;
    });

    // Step 6 Logic
    document.getElementById('btnBackStep6').addEventListener('click', () => {
        document.getElementById('step6-card').style.display = 'none';
        document.getElementById('step5-card').style.display = 'block';
        
        const step5 = document.getElementById('stepper-5');
        step5.classList.add('active');
        step5.querySelector('.step-circle').innerHTML = '5';
        step5.querySelector('.step-circle').style.backgroundColor = '';
        
        const step6 = document.getElementById('stepper-6');
        step6.classList.remove('active');
        step6.classList.add('inactive');
    });

    document.getElementById('btnContinueStep6').addEventListener('click', () => {
        const checkpoints = document.getElementById('checkpointsCount').value;
        const timing = document.getElementById('checkpointTiming').value;
        const minAtt = document.getElementById('minAttendance').value;
        const qrRefresh = document.getElementById('qrRefresh').value;

        if (!checkpoints || !minAtt || !qrRefresh) {
            alert('Please fill out all attendance rules.');
            return;
        }

        eventDraft.checkpoints_count = parseInt(checkpoints, 10);
        eventDraft.checkpoint_timing = timing;
        eventDraft.min_attendance_percent = parseInt(minAtt, 10);
        eventDraft.qr_refresh_interval_sec = parseInt(qrRefresh, 10);

        // Update Preview
        document.getElementById('previewTitle').textContent = eventDraft.title || 'Untitled event';
        document.getElementById('previewCategory').textContent = eventDraft.category || 'Event';
        document.getElementById('previewDescription').textContent = eventDraft.description || 'No description added yet.';
        
        let formattedStartDate = eventDraft.start_date || '';
        document.getElementById('previewSchedule').textContent = `${formattedStartDate} · ${eventDraft.start_time || ''}–${eventDraft.end_time || ''}`;
        document.getElementById('previewVenue').textContent = eventDraft.venue_name || 'No venue';
        document.getElementById('previewGeofence').textContent = `${eventDraft.attendance_radius_meters || 0} m radius`;
        document.getElementById('previewGuests').textContent = `${(eventDraft.guests || []).length} added`;
        document.getElementById('previewSessions').textContent = `${(eventDraft.sessions || []).length} added`;
        document.getElementById('previewRules').textContent = `${eventDraft.checkpoints_count || 0} checkpoints · ${eventDraft.min_attendance_percent || 0}% minimum · ${eventDraft.qr_refresh_interval_sec || 10}s QR`;

        // Transition to Step 7
        document.getElementById('step6-card').style.display = 'none';
        document.getElementById('step7-card').style.display = 'block';
        
        const step6 = document.getElementById('stepper-6');
        step6.classList.remove('active');
        step6.querySelector('.step-circle').innerHTML = '✓';
        step6.querySelector('.step-circle').style.backgroundColor = '#00b050';
        step6.querySelector('.step-circle').style.color = 'white';
        
        const step7 = document.getElementById('stepper-7');
        step7.classList.remove('inactive');
        step7.classList.add('active');
    });

    // Step 7 Logic
    document.getElementById('btnBackStep7').addEventListener('click', () => {
        document.getElementById('step7-card').style.display = 'none';
        document.getElementById('step6-card').style.display = 'block';
        
        const step6 = document.getElementById('stepper-6');
        step6.classList.add('active');
        step6.querySelector('.step-circle').innerHTML = '6';
        step6.querySelector('.step-circle').style.backgroundColor = '';
        
        const step7 = document.getElementById('stepper-7');
        step7.classList.remove('active');
        step7.classList.add('inactive');
    });

    document.getElementById('btnPublishEvent').addEventListener('click', async () => {
        const btnPublish = document.getElementById('btnPublishEvent');
        btnPublish.textContent = 'Publishing...';
        btnPublish.disabled = true;

        try {
            const { data: { session }, error: sessionError } = await supabase.auth.getSession();
            if (sessionError || !session) {
                throw new Error('Not logged in');
            }
            const user = session.user;

            // 1. Insert Event
            const { data: eventData, error: eventError } = await supabase
                .from('events')
                .insert({
                    organizer_id: user.id,
                    title: eventDraft.title,
                    description: eventDraft.description,
                    category: eventDraft.category,
                    banner_image_url: eventDraft.banner_image_url,
                    start_date: eventDraft.start_date,
                    end_date: eventDraft.end_date,
                    start_time: eventDraft.start_time,
                    end_time: eventDraft.end_time,
                    venue_name: eventDraft.venue_name,
                    address: eventDraft.address,
                    latitude: eventDraft.latitude,
                    longitude: eventDraft.longitude,
                    attendance_radius_meters: eventDraft.attendance_radius_meters,
                    checkpoints_count: eventDraft.checkpoints_count,
                    checkpoint_timing: eventDraft.checkpoint_timing,
                    min_attendance_percent: eventDraft.min_attendance_percent,
                    qr_refresh_interval_sec: eventDraft.qr_refresh_interval_sec
                })
                .select()
                .single();
            
            if (eventError) throw eventError;
            const eventId = eventData.id;

            // 2. Insert Guests
            if (eventDraft.guests && eventDraft.guests.length > 0) {
                const guestsToInsert = [];
                for (const guest of eventDraft.guests) {
                    let photoUrl = null;
                    if (guest.file) {
                        // VULN-004 FIX: Validate guest photo
                        try { validateImageFile(guest.file); } catch { /* skip invalid files */ }
                        const fileExt = guest.file.name.split('.').pop().toLowerCase();
                        // VULN-016 FIX: Secure random filename
                        const fileName = `${crypto.randomUUID()}.${fileExt}`;
                        const filePath = `${user.id}/${eventId}/${fileName}`;
                        const { error: uploadError } = await supabase.storage.from('guest_photos').upload(filePath, guest.file);
                        if (!uploadError) {
                            photoUrl = supabase.storage.from('guest_photos').getPublicUrl(filePath).data.publicUrl;
                        }
                    }
                    guestsToInsert.push({
                        event_id: eventId,
                        name: guest.name,
                        designation: guest.designation,
                        description: guest.description,
                        photo_url: photoUrl
                    });
                }
                const { error: guestError } = await supabase.from('event_guests').insert(guestsToInsert);
                if (guestError) console.error("Guest error", guestError);
            }

            // 3. Insert Sessions
            if (eventDraft.sessions && eventDraft.sessions.length > 0) {
                const sessionsToInsert = eventDraft.sessions.map(s => ({
                    event_id: eventId,
                    name: s.name,
                    speaker: s.speaker,
                    start_time: s.start_time,
                    end_time: s.end_time,
                    room: s.room
                }));
                const { error: sessionError } = await supabase.from('event_sessions').insert(sessionsToInsert);
                if (sessionError) console.error("Session error", sessionError);
            }

            alert('Event successfully created and published!');
            window.location.href = 'events.html';
        } catch (err) {
            console.error('Error creating event:', err);
            alert('Failed to publish event: ' + err.message);
            btnPublish.textContent = 'Create Event';
            btnPublish.disabled = false;
        }
    });
});
