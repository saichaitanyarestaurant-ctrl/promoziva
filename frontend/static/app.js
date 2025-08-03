// AI Orchestrator Frontend Application
class AIOrchestratorApp {
    constructor() {
        this.apiBaseUrl = window.location.origin + '/api/v1';
        this.currentTaskId = null;
        this.pollingInterval = null;
        this.isConnected = false;
        
        this.initializeElements();
        this.bindEvents();
        this.checkConnection();
        this.startPolling();
    }

    initializeElements() {
        // Form elements
        this.commandForm = document.getElementById('command-form');
        this.commandInput = document.getElementById('command-input');
        this.submitBtn = document.getElementById('submit-btn');
        
        // Status elements
        this.connectionStatus = document.getElementById('connection-status');
        this.refreshBtn = document.getElementById('refresh-btn');
        this.refreshTasksBtn = document.getElementById('refresh-tasks-btn');
        this.clearLogBtn = document.getElementById('clear-log-btn');
        
        // Content elements
        this.currentTaskDiv = document.getElementById('current-task');
        this.tasksList = document.getElementById('tasks-list');
        this.conversationHistory = document.getElementById('conversation-history');
        this.apiLog = document.getElementById('api-log');
        
        // Queue status elements
        this.pendingCount = document.getElementById('pending-count');
        this.processingCount = document.getElementById('processing-count');
        this.completedCount = document.getElementById('completed-count');
        this.failedCount = document.getElementById('failed-count');
        
        // Overlay and toast
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.toast = document.getElementById('toast');
        this.toastIcon = document.getElementById('toast-icon');
        this.toastTitle = document.getElementById('toast-title');
        this.toastMessage = document.getElementById('toast-message');
    }

    bindEvents() {
        // Form submission
        this.commandForm.addEventListener('submit', (e) => this.handleCommandSubmit(e));
        
        // Button clicks
        this.refreshBtn.addEventListener('click', () => this.refreshAll());
        this.refreshTasksBtn.addEventListener('click', () => this.loadTasks());
        this.clearLogBtn.addEventListener('click', () => this.clearApiLog());
        
        // Auto-resize textarea
        this.commandInput.addEventListener('input', () => this.autoResizeTextarea());
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
    }

    async checkConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            if (response.ok) {
                this.setConnectionStatus('connected');
                this.isConnected = true;
            } else {
                this.setConnectionStatus('error');
                this.isConnected = false;
            }
        } catch (error) {
            this.setConnectionStatus('error');
            this.isConnected = false;
            this.logApiInteraction('error', 'Failed to connect to API', error.message);
        }
    }

    setConnectionStatus(status) {
        const indicator = this.connectionStatus.querySelector('div');
        const text = this.connectionStatus.querySelector('span');
        
        indicator.className = 'w-3 h-3 rounded-full mr-2';
        
        switch (status) {
            case 'connected':
                indicator.classList.add('connection-connected');
                text.textContent = 'Connected';
                break;
            case 'connecting':
                indicator.classList.add('connection-connecting');
                text.textContent = 'Connecting...';
                break;
            case 'error':
                indicator.classList.add('connection-error');
                text.textContent = 'Connection Error';
                break;
        }
    }

    async handleCommandSubmit(e) {
        e.preventDefault();
        
        const command = this.commandInput.value.trim();
        if (!command) {
            this.showToast('error', 'Error', 'Please enter a command');
            return;
        }

        if (!this.isConnected) {
            this.showToast('error', 'Error', 'Not connected to API');
            return;
        }

        this.showLoading(true);
        this.submitBtn.disabled = true;

        try {
            this.logApiInteraction('info', 'Submitting command', command);
            
            const response = await fetch(`${this.apiBaseUrl}/command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    command: command,
                    user_id: 1, // Default user ID
                    context: {}
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.logApiInteraction('success', 'Command submitted successfully', `Task ID: ${data.task_id}`);
                this.showToast('success', 'Success', 'Command submitted successfully');
                this.currentTaskId = data.task_id;
                this.commandInput.value = '';
                this.autoResizeTextarea();
                
                // Update UI immediately
                await this.refreshAll();
            } else {
                throw new Error(data.detail || 'Failed to submit command');
            }
        } catch (error) {
            this.logApiInteraction('error', 'Command submission failed', error.message);
            this.showToast('error', 'Error', error.message);
        } finally {
            this.showLoading(false);
            this.submitBtn.disabled = false;
        }
    }

    async refreshAll() {
        await Promise.all([
            this.loadQueueStatus(),
            this.loadTasks(),
            this.loadConversationHistory()
        ]);
    }

    async loadQueueStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/queue/status`);
            if (response.ok) {
                const data = await response.json();
                this.updateQueueStatus(data);
            }
        } catch (error) {
            this.logApiInteraction('error', 'Failed to load queue status', error.message);
        }
    }

    updateQueueStatus(data) {
        this.pendingCount.textContent = data.total_pending || 0;
        this.processingCount.textContent = data.total_processing || 0;
        this.completedCount.textContent = data.total_completed || 0;
        this.failedCount.textContent = data.total_failed || 0;
    }

    async loadTasks() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/tasks?limit=10`);
            if (response.ok) {
                const tasks = await response.json();
                this.renderTasks(tasks);
            }
        } catch (error) {
            this.logApiInteraction('error', 'Failed to load tasks', error.message);
        }
    }

    renderTasks(tasks) {
        if (tasks.length === 0) {
            this.tasksList.innerHTML = '<div class="text-gray-500 text-center py-8">No tasks yet</div>';
            return;
        }

        this.tasksList.innerHTML = tasks.map(task => `
            <div class="task-card">
                <div class="flex items-center justify-between mb-2">
                    <h3 class="font-semibold text-gray-900">${this.escapeHtml(task.title)}</h3>
                    <span class="px-2 py-1 text-xs font-medium rounded-full status-${task.status}">
                        ${task.status}
                    </span>
                </div>
                <p class="text-sm text-gray-600 mb-2">${this.escapeHtml(task.description || '')}</p>
                <div class="flex items-center justify-between text-xs text-gray-500">
                    <span>ID: ${task.task_id}</span>
                    <span>${this.formatDate(task.created_at)}</span>
                </div>
                ${task.error_message ? `
                    <div class="mt-2 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-700">
                        Error: ${this.escapeHtml(task.error_message)}
                    </div>
                ` : ''}
                ${task.result ? `
                    <div class="mt-2 p-2 bg-green-50 border border-green-200 rounded text-sm">
                        <strong>Result:</strong> ${this.escapeHtml(JSON.stringify(task.result, null, 2))}
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    async loadConversationHistory() {
        try {
            // For now, we'll show a placeholder since conversation history needs to be implemented
            this.conversationHistory.innerHTML = '<div class="text-gray-500 text-center py-8">No conversation history</div>';
        } catch (error) {
            this.logApiInteraction('error', 'Failed to load conversation history', error.message);
        }
    }

    logApiInteraction(type, title, message) {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = `api-log-entry api-log-${type}`;
        logEntry.innerHTML = `
            <span class="text-gray-500">[${timestamp}]</span>
            <span class="font-medium">${title}:</span>
            <span>${this.escapeHtml(message)}</span>
        `;
        
        // Remove placeholder if it exists
        const placeholder = this.apiLog.querySelector('.text-gray-500');
        if (placeholder && placeholder.textContent === 'No API interactions yet') {
            this.apiLog.innerHTML = '';
        }
        
        this.apiLog.appendChild(logEntry);
        this.apiLog.scrollTop = this.apiLog.scrollHeight;
    }

    clearApiLog() {
        this.apiLog.innerHTML = '<div class="text-gray-500">No API interactions yet</div>';
    }

    showLoading(show) {
        if (show) {
            this.loadingOverlay.classList.remove('hidden');
        } else {
            this.loadingOverlay.classList.add('hidden');
        }
    }

    showToast(type, title, message) {
        this.toastTitle.textContent = title;
        this.toastMessage.textContent = message;
        
        // Set icon based on type
        this.toastIcon.innerHTML = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
        
        // Show toast
        this.toast.classList.remove('hidden');
        this.toast.classList.add('toast-enter');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.toast.classList.add('toast-exit');
            setTimeout(() => {
                this.toast.classList.add('hidden');
                this.toast.classList.remove('toast-enter', 'toast-exit');
            }, 300);
        }, 5000);
    }

    startPolling() {
        // Poll for updates every 5 seconds
        this.pollingInterval = setInterval(() => {
            if (this.isConnected) {
                this.loadQueueStatus();
                this.loadTasks();
            }
        }, 5000);
    }

    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    }

    autoResizeTextarea() {
        this.commandInput.style.height = 'auto';
        this.commandInput.style.height = this.commandInput.scrollHeight + 'px';
    }

    handleKeyboardShortcuts(e) {
        // Ctrl+Enter to submit command
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            this.commandForm.dispatchEvent(new Event('submit'));
        }
        
        // Escape to clear command
        if (e.key === 'Escape') {
            this.commandInput.value = '';
            this.autoResizeTextarea();
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleString();
    }

    // Cleanup method
    destroy() {
        this.stopPolling();
        // Remove event listeners if needed
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.aiOrchestratorApp = new AIOrchestratorApp();
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (window.aiOrchestratorApp) {
        window.aiOrchestratorApp.destroy();
    }
});