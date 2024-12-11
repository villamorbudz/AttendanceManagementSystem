document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('leaveRequestModal');
    const modalContent = document.getElementById('modalContent');
    const newLeaveBtn = document.getElementById('newLeaveBtn');
    const closeModalBtn = document.getElementById('closeModal');
    const cancelBtn = document.getElementById('cancelLeaveRequest');
    const form = document.getElementById('leaveRequestForm');
    const errorMessage = document.getElementById('errorMessage');

    function showModal() {
        modal.classList.remove('hidden');
        setTimeout(() => {
            modal.classList.add('opacity-100');
            modalContent.classList.remove('opacity-0', 'translate-y-4');
            modalContent.classList.add('opacity-100', 'translate-y-0');
        }, 10);
    }

    function hideModal() {
        modal.classList.remove('opacity-100');
        modalContent.classList.remove('opacity-100', 'translate-y-0');
        modalContent.classList.add('opacity-0', 'translate-y-4');
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 300);
        form.reset();
        errorMessage.classList.add('hidden');
        errorMessage.textContent = '';
    }

    function validateDates(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (start < today) {
            return "Start date cannot be in the past";
        }
        if (end < start) {
            return "End date must be after or equal to start date";
        }
        return "";
    }

    newLeaveBtn?.addEventListener('click', showModal);
    closeModalBtn?.addEventListener('click', hideModal);
    cancelBtn?.addEventListener('click', hideModal);

    // Close modal when clicking outside
    modal?.addEventListener('click', function(e) {
        if (e.target === modal) {
            hideModal();
        }
    });

    form?.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const startDate = formData.get('startDate');
        const endDate = formData.get('endDate');
        const reason = formData.get('reason');
        
        // Validate dates
        const dateError = validateDates(startDate, endDate);
        if (dateError) {
            errorMessage.textContent = dateError;
            errorMessage.classList.remove('hidden');
            return;
        }

        // Validate reason length
        if (reason.length < 10) {
            errorMessage.textContent = "Please provide a more detailed reason (at least 10 characters)";
            errorMessage.classList.remove('hidden');
            return;
        }

        // If all validations pass, submit the form
        // TODO: Add your form submission logic here
        console.log('Form submitted:', Object.fromEntries(formData));
        hideModal();
    });

    // Set minimum date for date inputs
    const today = new Date().toISOString().split('T')[0];
    document.querySelector('input[name="startDate"]').min = today;
    document.querySelector('input[name="endDate"]').min = today;

    // Update end date min value when start date changes
    document.querySelector('input[name="startDate"]').addEventListener('change', function(e) {
        document.querySelector('input[name="endDate"]').min = e.target.value;
    });
});
