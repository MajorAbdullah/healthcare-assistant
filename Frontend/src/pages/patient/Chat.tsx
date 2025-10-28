import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Send, Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

const suggestedQuestions = [
  "What causes high blood pressure?",
  "How to manage diabetes?",
  "Symptoms of stroke?",
  "Healthy diet tips?",
];

const MedicalChat = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (messageText?: string) => {
    const text = messageText || input.trim();
    if (!text) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: getAIResponse(text),
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
      setIsLoading(false);
    }, 1500);
  };

  const getAIResponse = (question: string): string => {
    const lowerQuestion = question.toLowerCase();
    
    if (lowerQuestion.includes("blood pressure")) {
      return "High blood pressure can be caused by several factors including:\n\n• Unhealthy diet (high sodium intake)\n• Lack of physical activity\n• Obesity\n• Excessive alcohol consumption\n• Stress\n• Genetics\n\nIt's important to monitor your blood pressure regularly and consult with a healthcare provider for personalized advice.";
    } else if (lowerQuestion.includes("diabetes")) {
      return "Managing diabetes involves:\n\n• Regular blood sugar monitoring\n• Following a balanced diet\n• Regular physical exercise\n• Taking medications as prescribed\n• Maintaining a healthy weight\n• Regular check-ups with your doctor\n\nAlways work closely with your healthcare team for the best management plan.";
    } else if (lowerQuestion.includes("stroke")) {
      return "Common stroke symptoms (FAST):\n\n• **F**ace drooping\n• **A**rm weakness\n• **S**peech difficulty\n• **T**ime to call emergency services\n\nOther symptoms may include:\n• Sudden numbness or weakness\n• Confusion or trouble speaking\n• Vision problems\n• Severe headache\n\nIf you suspect a stroke, call emergency services immediately.";
    } else if (lowerQuestion.includes("diet") || lowerQuestion.includes("healthy")) {
      return "Healthy diet tips:\n\n• Eat plenty of fruits and vegetables\n• Choose whole grains over refined grains\n• Include lean proteins (fish, poultry, legumes)\n• Limit saturated fats and trans fats\n• Reduce sodium intake\n• Stay hydrated with water\n• Control portion sizes\n\nConsider consulting a nutritionist for a personalized meal plan.";
    }
    
    return "Thank you for your question. While I can provide general health information, I recommend consulting with a healthcare professional for personalized medical advice. Is there a specific health topic you'd like to learn more about?";
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="glass-header sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Button variant="ghost" onClick={() => navigate("/patient/dashboard")}>
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back
          </Button>
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-semibold">Medical Assistant</h1>
            <Badge variant="secondary" className="gap-1">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              Online
            </Badge>
          </div>
          <div className="w-20" />
        </div>
      </header>

      {/* Chat Container */}
      <main className="flex-1 container mx-auto px-4 py-6 max-w-4xl flex flex-col">
        {/* Messages Area */}
        <Card className="glass-card flex-1 flex flex-col overflow-hidden mb-4">
          <CardContent className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 ? (
              <div className="h-full flex items-center justify-center">
                <div className="text-center space-y-6">
                  <div className="flex justify-center">
                    <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center">
                      <Bot className="w-10 h-10 text-primary" />
                    </div>
                  </div>
                  <div>
                    <h3 className="text-2xl font-semibold mb-2">How can I help you today?</h3>
                    <p className="text-muted-foreground">Ask me any medical question</p>
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Try asking:</p>
                    <div className="flex flex-wrap gap-2 justify-center">
                      {suggestedQuestions.map((question, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          size="sm"
                          onClick={() => handleSendMessage(question)}
                          className="text-xs"
                        >
                          {question}
                        </Button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={cn(
                      "flex gap-3",
                      message.role === "user" ? "justify-end" : "justify-start"
                    )}
                  >
                    {message.role === "assistant" && (
                      <Avatar className="w-8 h-8 flex-shrink-0">
                        <AvatarFallback className="bg-primary text-primary-foreground">
                          <Bot className="w-4 h-4" />
                        </AvatarFallback>
                      </Avatar>
                    )}
                    <div
                      className={cn(
                        "max-w-[70%] rounded-2xl px-4 py-3",
                        message.role === "user"
                          ? "bg-primary text-primary-foreground"
                          : "bg-gray-100 text-gray-900"
                      )}
                    >
                      <p className="whitespace-pre-wrap text-sm">{message.content}</p>
                      <p
                        className={cn(
                          "text-xs mt-1",
                          message.role === "user" ? "text-primary-foreground/70" : "text-muted-foreground"
                        )}
                      >
                        {message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                      </p>
                    </div>
                    {message.role === "user" && (
                      <Avatar className="w-8 h-8 flex-shrink-0">
                        <AvatarFallback className="bg-secondary text-secondary-foreground">
                          <User className="w-4 h-4" />
                        </AvatarFallback>
                      </Avatar>
                    )}
                  </div>
                ))}
                {isLoading && (
                  <div className="flex gap-3 justify-start">
                    <Avatar className="w-8 h-8">
                      <AvatarFallback className="bg-primary text-primary-foreground">
                        <Bot className="w-4 h-4" />
                      </AvatarFallback>
                    </Avatar>
                    <div className="bg-gray-100 rounded-2xl px-4 py-3">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </CardContent>
        </Card>

        {/* Input Area */}
        <Card className="glass-card">
          <CardContent className="p-4">
            <div className="flex gap-2">
              <Input
                placeholder="Ask a medical question..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
                className="flex-1"
              />
              <Button
                onClick={() => handleSendMessage()}
                disabled={!input.trim() || isLoading}
                size="icon"
                className="flex-shrink-0"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default MedicalChat;
