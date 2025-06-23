// Dashboard JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    initializeDashboard();
    
    // Auto-refresh data every 5 minutes
    setInterval(refreshDashboardData, 300000);
    
    // Add click handlers for metric cards
    addMetricCardHandlers();
    
    // Initialize tooltips
    initializeTooltips();
});

function initializeDashboard() {
    console.log('Dashboard initialized');
    
    // Add loading states
    showLoadingStates();
    
    // Load initial data
    loadDashboardData();
    
    // Setup real-time updates
    setupRealTimeUpdates();
}

function loadDashboardData() {
    // Simulate loading dashboard data
    setTimeout(() => {
        hideLoadingStates();
        animateMetrics();
    }, 1000);
}

function refreshDashboardData() {
    console.log('Refreshing dashboard data...');
    
    // Add refresh indicator
    showRefreshIndicator();
    
    // Simulate API call
    setTimeout(() => {
        hideRefreshIndicator();
        updateMetrics();
    }, 2000);
}

function showLoadingStates() {
    const metricCards = document.querySelectorAll('.metric-card');
    metricCards.forEach(card => {
        const value = card.querySelector('.metric-value');
        if (value) {
            value.innerHTML = '<div class="loading-spinner"></div>';
        }
    });
}

function hideLoadingStates() {
    const spinners = document.querySelectorAll('.loading-spinner');
    spinners.forEach(spinner => {
        spinner.remove();
    });
}

function animateMetrics() {
    const metricValues = document.querySelectorAll('.metric-value');
    metricValues.forEach(value => {
        const finalValue = value.textContent;
        const numericValue = parseInt(finalValue.replace(/[^0-9]/g, ''));
        
        if (!isNaN(numericValue)) {
            animateCounter(value, 0, numericValue, 1000);
        }
    });
}

function animateCounter(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        
        // Format the number based on original format
        const originalText = element.getAttribute('data-original') || element.textContent;
        if (originalText.includes('$')) {
            element.textContent = '$' + Math.floor(current).toLocaleString();
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, 16);
}

function addMetricCardHandlers() {
    const metricCards = document.querySelectorAll('.metric-card');
    metricCards.forEach(card => {
        card.addEventListener('click', function() {
            const label = this.querySelector('.metric-label').textContent;
            showMetricDetails(label);
        });
        
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 16px rgba(0,0,0,0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
        });
    });
}

function showMetricDetails(metricType) {
    // Create modal or navigate to detailed view
    console.log('Showing details for:', metricType);
    
    // Example: Show a simple alert (replace with modal)
    alert(`Detailed view for ${metricType} would open here`);
}

function setupRealTimeUpdates() {
    // Setup WebSocket connection for real-time updates
    if (typeof WebSocket !== 'undefined') {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/admin/dashboard/`;
        
        try {
            const socket = new WebSocket(wsUrl);
            
            socket.onopen = function(event) {
                console.log('Dashboard WebSocket connected');
            };
            
            socket.onmessage = function(event) {
                const data = JSON.parse(event.data);
                handleRealTimeUpdate(data);
            };
            
            socket.onclose = function(event) {
                console.log('Dashboard WebSocket disconnected');
                // Attempt to reconnect after 5 seconds
                setTimeout(setupRealTimeUpdates, 5000);
            };
            
            socket.onerror = function(error) {
                console.error('Dashboard WebSocket error:', error);
            };
        } catch (error) {
            console.log('WebSocket not available, using polling instead');
            // Fallback to polling
            setInterval(refreshDashboardData, 30000);
        }
    }
}

function handleRealTimeUpdate(data) {
    console.log('Real-time update received:', data);
    
    // Update specific metrics based on the data
    if (data.type === 'metric_update') {
        updateMetricValue(data.metric, data.value);
    } else if (data.type === 'new_activity') {
        addNewActivity(data.activity);
    }
}

function updateMetricValue(metricName, newValue) {
    const metricCard = document.querySelector(`[data-metric="${metricName}"]`);
    if (metricCard) {
        const valueElement = metricCard.querySelector('.metric-value');
        if (valueElement) {
            // Animate the change
            valueElement.style.color = '#28a745';
            valueElement.textContent = newValue;
            
            setTimeout(() => {
                valueElement.style.color = '#007cba';
            }, 1000);
        }
    }
}

function addNewActivity(activity) {
    const activitiesList = document.querySelector('.recent-activities');
    if (activitiesList) {
        const activityElement = createActivityElement(activity);
        activitiesList.insertBefore(activityElement, activitiesList.firstChild);
        
        // Remove oldest activity if more than 10
        const activities = activitiesList.querySelectorAll('.activity-item');
        if (activities.length > 10) {
            activities[activities.length - 1].remove();
        }
        
        // Highlight new activity
        activityElement.style.backgroundColor = '#e3f2fd';
        setTimeout(() => {
            activityElement.style.backgroundColor = '';
        }, 3000);
    }
}

function createActivityElement(activity) {
    const div = document.createElement('div');
    div.className = 'activity-item';
    div.innerHTML = `
        <strong>${activity.user}</strong>
        <span>${activity.action}</span>
        <br>
        <small style="color: #666;">Just now</small>
    `;
    return div;
}

function showRefreshIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'refresh-indicator';
    indicator.innerHTML = '🔄 Refreshing...';
    indicator.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #007cba;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        z-index: 9999;
        animation: fadeIn 0.3s ease;
    `;
    document.body.appendChild(indicator);
}

function hideRefreshIndicator() {
    const indicator = document.getElementById('refresh-indicator');
    if (indicator) {
        indicator.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            indicator.remove();
        }, 300);
    }
}

function updateMetrics() {
    // Simulate metric updates
    const metrics = [
        { selector: '[data-metric="users"] .metric-value', value: Math.floor(Math.random() * 1000) + 5000 },
        { selector: '[data-metric="courses"] .metric-value', value: Math.floor(Math.random() * 100) + 500 },
        { selector: '[data-metric="revenue"] .metric-value', value: '$' + (Math.floor(Math.random() * 10000) + 50000).toLocaleString() }
    ];
    
    metrics.forEach(metric => {
        const element = document.querySelector(metric.selector);
        if (element) {
            element.textContent = metric.value;
            // Add update animation
            element.style.transform = 'scale(1.1)';
            element.style.color = '#28a745';
            setTimeout(() => {
                element.style.transform = 'scale(1)';
                element.style.color = '#007cba';
            }, 500);
        }
    });
}

function initializeTooltips() {
    // Add tooltips to metric cards
    const metricCards = document.querySelectorAll('.metric-card');
    metricCards.forEach(card => {
        const label = card.querySelector('.metric-label').textContent;
        card.title = `Click to view detailed ${label.toLowerCase()} analytics`;
    });
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-10px); }
    }
    
    .metric-card {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .activity-item {
        transition: background-color 0.3s ease;
    }
`;
document.head.appendChild(style);