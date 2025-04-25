// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle image preview for file inputs
    const imageInputs = document.querySelectorAll('input[type="file"][accept="image/*"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                const preview = document.getElementById(`${this.id}-preview`);
                
                reader.onload = function(e) {
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                }
                
                reader.readAsDataURL(file);
            }
        });
    });

    // Handle form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Handle dynamic form fields
    document.querySelectorAll('.add-form-row').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const template = document.getElementById(this.dataset.template);
            const container = document.getElementById(this.dataset.container);
            const newRow = template.content.cloneNode(true);
            container.appendChild(newRow);
        });
    });

    // Handle delete buttons
    document.querySelectorAll('.delete-row').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            this.closest('.form-row').remove();
        });
    });
}); 