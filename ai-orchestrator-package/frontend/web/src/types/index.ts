export interface Task {
  task_id: number;
  title: string;
  status: string;
  created_at?: string;
  started_at?: string;
  completed_at?: string;
  result?: any;
  error_message?: string;
}

export interface QueueStatus {
  queue_size: number;
  active_tasks: number;
  max_concurrent_tasks: number;
  total_pending: number;
  total_processing: number;
  total_completed: number;
  total_failed: number;
}

export interface ServiceHealth {
  services: {
    [key: string]: boolean;
  };
}

export interface CommandRequest {
  command: string;
  user_id?: number;
  conversation_id?: number;
  context?: Record<string, any>;
}

export interface CommandResponse {
  task_id: number;
  status: string;
  message: string;
  estimated_completion?: string;
}

export interface Conversation {
  conversation_id: number;
  title: string;
  created_at: string;
  messages: ConversationMessage[];
}

export interface ConversationMessage {
  id: number;
  content: string;
  role: string;
  timestamp: string;
}