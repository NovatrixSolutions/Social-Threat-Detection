// Initialize Vanta.js background
document.addEventListener('DOMContentLoaded', function() {
    VANTA.NET({
        el: "#vanta-bg",
        color: 0x0072ff,
        backgroundColor: 0x021027,
        points: 12.00,
        maxDistance: 22.00,
        spacing: 18.00
    });

    // Terms agreement functionality
    document.getElementById('agreeBtn').addEventListener('click', function() {
        document.querySelector('.disclaimer-box').style.display = 'none';
        document.getElementById('detectSection').style.display = 'block';
    });

    // Threat detection button
    document.getElementById('detectBtn').addEventListener('click', function() {
        
        this.disabled = true;
    
        // Simulate scanning process
        setTimeout(() => {window.location.href = "detection.html"; // Navigate to results page
    }, 2000); 
    });
    
});