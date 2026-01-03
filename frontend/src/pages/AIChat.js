import { useState, useEffect, useRef } from 'react';
import { DashboardLayout } from './Dashboard';
import { api } from '../utils/api';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { MessageSquare, Send, Bot, User as UserIcon, Loader2 } from 'lucide-react';

function AIChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await api.getChatHistory();
      setMessages(response.data);
    } catch (error) {
      if (error.response?.status !== 404) {
        toast.error('Failed to load chat history');
      }
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    setSending(true);

    // Add user message immediately
    setMessages(prev => [...prev, {
      role: 'user',
      content: userMessage,
      timestamp: new Date().toISOString()
    }]);

    try {
      const response = await api.sendChatMessage(userMessage);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date().toISOString()
      }]);
    } catch (error) {
      toast.error('Failed to send message');
    } finally {
      setSending(false);
    }
  };

  return (
    <DashboardLayout active="/ai-chat">
      <div className="h-screen flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-stone-200 p-6">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-emerald-100 flex items-center justify-center">
              <Bot className="h-6 w-6 text-emerald-900" />
            </div>
            <div>
              <h1 data-testid="ai-chat-title" className="text-2xl font-semibold text-stone-900">
                AI Financial Advisor
              </h1>
              <p className="text-sm text-stone-600">Your personal 24/7 wealth growth partner</p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 bg-stone-50">
          {loading ? (
            <div className="text-center py-12">
              <p className="text-stone-500">Loading conversation...</p>
            </div>
          ) : messages.length === 0 ? (
            <div className="text-center py-12">
              <MessageSquare className="h-16 w-16 text-stone-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-stone-900 mb-2">Start a Conversation</h3>
              <p className="text-stone-600 max-w-md mx-auto">
                Ask me anything about budgeting, investing, income generation, or financial planning!
              </p>
            </div>
          ) : (
            <div className="max-w-4xl mx-auto space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  data-testid={`chat-message-${index}`}
                  className={`flex gap-3 ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  {message.role === 'assistant' && (
                    <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0">
                      <Bot className="h-5 w-5 text-emerald-900" />
                    </div>
                  )}
                  <div
                    className={`max-w-2xl rounded-2xl p-4 ${
                      message.role === 'user'
                        ? 'bg-emerald-900 text-white'
                        : 'bg-white border border-stone-200 text-stone-900'
                    }`}
                  >
                    <p className="leading-relaxed whitespace-pre-wrap">{message.content}</p>
                  </div>
                  {message.role === 'user' && (
                    <div className="w-8 h-8 rounded-full bg-lime-200 flex items-center justify-center flex-shrink-0">
                      <UserIcon className="h-5 w-5 text-emerald-900" />
                    </div>
                  )}
                </div>
              ))}
              {sending && (
                <div className="flex gap-3 justify-start">
                  <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0">
                    <Bot className="h-5 w-5 text-emerald-900" />
                  </div>
                  <div className="bg-white border border-stone-200 rounded-2xl p-4">
                    <Loader2 className="h-5 w-5 text-stone-400 animate-spin" />
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input */}
        <div className="bg-white border-t border-stone-200 p-6">
          <form onSubmit={sendMessage} className="max-w-4xl mx-auto">
            <div className="flex gap-3">
              <Input
                data-testid="chat-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask me anything about your finances..."
                className="flex-1 rounded-full px-6"
                disabled={sending}
              />
              <Button
                data-testid="send-message-btn"
                type="submit"
                disabled={sending || !input.trim()}
                className="btn-primary px-6"
              >
                <Send className="h-5 w-5" />
              </Button>
            </div>
          </form>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default AIChat;
