/**
 * OmniEvent - Main Client-Side Logic
 * Implements real-time grid filtering, category switching, form validation,
 * and elegant UX micro-interactions.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Cache UI elements
    const searchInput = document.getElementById("search-input");
    const chips = document.querySelectorAll(".chip");
    const eventCards = document.querySelectorAll(".event-card");
    const emptyState = document.getElementById("empty-state-view");
    const sessionCountBadge = document.getElementById("session-count-badge");
    const createForm = document.getElementById("create-event-form");
    const errorBanner = document.getElementById("form-validation-error");
    const errorMessageText = document.getElementById("error-message-text");

    // Initialize state
    let activeCategory = "all";
    let searchQuery = "";

    // ----------------------------------------------------------------------
    // Real-Time Grid Filtering & Search
    // ----------------------------------------------------------------------
    const updateGridVisibility = () => {
        let visibleCount = 0;

        eventCards.forEach(card => {
            const cardCategory = card.getAttribute("data-category");
            const title = card.getAttribute("data-title") || "";
            const speaker = card.getAttribute("data-speaker") || "";
            const location = card.getAttribute("data-location") || "";
            const description = card.getAttribute("data-description") || "";

            // Matches category criteria
            const matchesCategory = (activeCategory === "all" || cardCategory === activeCategory);

            // Matches search criteria
            const matchesSearch = !searchQuery || 
                title.includes(searchQuery) ||
                speaker.includes(searchQuery) ||
                location.includes(searchQuery) ||
                description.includes(searchQuery);

            if (matchesCategory && matchesSearch) {
                card.style.display = "flex";
                card.style.opacity = "1";
                card.style.transform = "scale(1)";
                visibleCount++;
            } else {
                card.style.display = "none";
                card.style.opacity = "0";
                card.style.transform = "scale(0.95)";
            }
        });

        // Toggle Empty State View
        if (visibleCount === 0) {
            if (emptyState) emptyState.style.display = "block";
        } else {
            if (emptyState) emptyState.style.display = "none";
        }

        // Update Dynamic Badge Counter
        if (sessionCountBadge) {
            sessionCountBadge.textContent = `${visibleCount} Session${visibleCount === 1 ? "" : "s"} Displayed`;
        }
    };

    // Category click handler
    chips.forEach(chip => {
        chip.addEventListener("click", () => {
            // Update active states
            chips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");

            activeCategory = chip.getAttribute("data-category");
            updateGridVisibility();
        });
    });

    // Real-time search keyup/input handler
    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            updateGridVisibility();
        });
    }

    // Global clear filters helper
    window.clearFilters = () => {
        if (searchInput) searchInput.value = "";
        searchQuery = "";
        
        chips.forEach(c => c.classList.remove("active"));
        const allChip = document.getElementById("filter-all");
        if (allChip) allChip.classList.add("active");
        
        activeCategory = "all";
        updateGridVisibility();
    };

    // ----------------------------------------------------------------------
    // Date & Time Form Validation
    // ----------------------------------------------------------------------
    if (createForm) {
        createForm.addEventListener("submit", (e) => {
            const startTimeInput = document.getElementById("start_time");
            const endTimeInput = document.getElementById("end_time");

            if (startTimeInput && endTimeInput) {
                const startTime = new Date(startTimeInput.value);
                const endTime = new Date(endTimeInput.value);

                if (startTime >= endTime) {
                    e.preventDefault(); // Stop form submission
                    
                    // Show elegant error banner
                    if (errorBanner && errorMessageText) {
                        errorMessageText.textContent = "The event end time must be after the start time.";
                        errorBanner.style.display = "flex";
                        errorBanner.scrollIntoView({ behavior: "smooth", block: "center" });
                    }
                    return;
                }
            }
            
            // Hide if successful
            if (errorBanner) {
                errorBanner.style.display = "none";
            }
        });
    }

    // ----------------------------------------------------------------------
    // Auto-Dismiss Toast Notifications
    // ----------------------------------------------------------------------
    const toasts = document.querySelectorAll(".toast");
    toasts.forEach(toast => {
        setTimeout(() => {
            // Smoothly fade out and remove
            toast.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            toast.style.opacity = "0";
            toast.style.transform = "translateY(-10px)";
            setTimeout(() => toast.remove(), 500);
        }, 5000); // 5 seconds
    });
});
