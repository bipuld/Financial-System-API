// Add this script to the Swagger UI template
window.onload = function() {
    const ui = SwaggerUIBundle({
        url: "/swagger.json", // or your Swagger schema URL
        dom_id: '#swagger-ui',
        presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIStandalonePreset
        ],
        layout: "StandaloneLayout",
        onComplete: function() {
            // Set token from localStorage
            const token = localStorage.getItem("swagger_bearer_token");
            if (token) {
                ui.preauthorizeApiKey("Authorization", token);
            }
        }
    });

    // Save token in localStorage on "Authorize" button
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('btn-done')) {
            const inputs = document.querySelectorAll('input[type="text"]');
            inputs.forEach(input => {
                if (input.placeholder.includes("Bearer")) {
                    localStorage.setItem("swagger_bearer_token", input.value);
                }
            });
        }
    });
};
