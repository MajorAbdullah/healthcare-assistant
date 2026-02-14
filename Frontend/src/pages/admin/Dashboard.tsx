import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { Shield, LogOut, Upload, FileText, Trash2, Database, CheckCircle2, XCircle, Loader2 } from "lucide-react";
import api from "@/lib/api";

interface UploadedDocument {
  id: string;
  filename: string;
  size: number;
  uploaded_at: string;
  status: 'indexed' | 'pending' | 'error';
  doc_type: string;
}

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [adminUsername, setAdminUsername] = useState("");
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [documents, setDocuments] = useState<UploadedDocument[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState({
    total_documents: 0,
    total_chunks: 0,
    collection_name: ""
  });

  useEffect(() => {
    const token = localStorage.getItem("admin_token");
    const username = localStorage.getItem("admin_username");
    
    if (!token) {
      toast.error("Please login first");
      navigate("/admin/auth");
      return;
    }
    
    setAdminUsername(username || "Admin");
    loadDocuments();
    loadStats();
  }, [navigate]);

  const loadDocuments = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('http://localhost:8000/api/v1/admin/documents');
      const result = await response.json();
      
      if (result.success && result.data) {
        setDocuments(result.data.documents || []);
      }
    } catch (error: any) {
      console.error("Failed to load documents:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/stats');
      const result = await response.json();
      
      if (result.success && result.data) {
        setStats(result.data);
      }
    } catch (error: any) {
      console.error("Failed to load stats:", error);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFiles(e.target.files);
    }
  };

  const handleUpload = async () => {
    if (!selectedFiles || selectedFiles.length === 0) {
      toast.error("Please select files to upload");
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    
    // Add all selected files
    Array.from(selectedFiles).forEach((file) => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/documents/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();

      if (result.success) {
        toast.success(`Successfully uploaded ${selectedFiles.length} file(s)! Indexing in progress...`);
        setSelectedFiles(null);
        // Reset file input
        const fileInput = document.getElementById('file-upload') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
        
        // Reload documents and stats
        loadDocuments();
        loadStats();
      } else {
        toast.error(result.message || "Upload failed");
      }
    } catch (error: any) {
      toast.error(error.message || "Upload failed");
      console.error("Upload error:", error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (docId: string, filename: string) => {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/v1/admin/documents/${docId}`, {
        method: 'DELETE',
      });

      const result = await response.json();

      if (result.success) {
        toast.success("Document deleted successfully");
        loadDocuments();
        loadStats();
      } else {
        toast.error(result.message || "Delete failed");
      }
    } catch (error: any) {
      toast.error(error.message || "Delete failed");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("admin_token");
    localStorage.removeItem("admin_username");
    navigate("/admin/auth");
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-purple-600 rounded-full flex items-center justify-center">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-semibold">Admin Panel</h1>
              <p className="text-sm text-muted-foreground">Welcome, {adminUsername}</p>
            </div>
          </div>
          <Button 
            variant="ghost" 
            size="icon"
            onClick={handleLogout}
          >
            <LogOut className="h-5 w-5" />
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Stats Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card className="shadow-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Total Documents
              </CardTitle>
              <FileText className="h-5 w-5 text-primary" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{stats.total_documents}</div>
            </CardContent>
          </Card>

          <Card className="shadow-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Indexed Chunks
              </CardTitle>
              <Database className="h-5 w-5 text-secondary" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{stats.total_chunks}</div>
            </CardContent>
          </Card>

          <Card className="shadow-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Collection
              </CardTitle>
              <Database className="h-5 w-5 text-accent" />
            </CardHeader>
            <CardContent>
              <div className="text-lg font-semibold truncate">{stats.collection_name || "medical_docs"}</div>
            </CardContent>
          </Card>
        </div>

        {/* Upload Section */}
        <Card className="shadow-card mb-8">
          <CardHeader>
            <CardTitle className="text-2xl flex items-center gap-2">
              <Upload className="h-6 w-6" />
              Upload Medical Documents
            </CardTitle>
            <CardDescription>
              Upload PDF, TXT, or Markdown files to enhance the AI knowledge base
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="file-upload">Select Files</Label>
              <Input
                id="file-upload"
                type="file"
                multiple
                accept=".pdf,.txt,.md"
                onChange={handleFileChange}
                disabled={isUploading}
              />
              {selectedFiles && selectedFiles.length > 0 && (
                <div className="text-sm text-muted-foreground">
                  {selectedFiles.length} file(s) selected
                </div>
              )}
            </div>

            <Button 
              onClick={handleUpload}
              disabled={!selectedFiles || isUploading}
              className="w-full md:w-auto"
            >
              {isUploading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Uploading & Indexing...
                </>
              ) : (
                <>
                  <Upload className="mr-2 h-4 w-4" />
                  Upload Documents
                </>
              )}
            </Button>

            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-900">
                <strong>ℹ️ Supported Formats:</strong> PDF (.pdf), Text (.txt), Markdown (.md)
              </p>
              <p className="text-sm text-blue-900 mt-1">
                Documents will be automatically processed, chunked, and indexed into the RAG vector database.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Documents List */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="text-2xl flex items-center gap-2">
              <FileText className="h-6 w-6" />
              Uploaded Documents
            </CardTitle>
            <CardDescription>
              Manage documents in the knowledge base
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : documents.length > 0 ? (
              <div className="space-y-3">
                {documents.map((doc) => (
                  <div 
                    key={doc.id}
                    className="flex items-center gap-4 p-4 border rounded-lg hover:shadow-md transition-shadow bg-white"
                  >
                    <FileText className="h-8 w-8 text-muted-foreground flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="font-medium truncate">{doc.filename}</div>
                      <div className="text-sm text-muted-foreground">
                        {formatFileSize(doc.size)} • {doc.doc_type} • {new Date(doc.uploaded_at).toLocaleDateString()}
                      </div>
                    </div>
                    <Badge 
                      variant={doc.status === 'indexed' ? 'default' : doc.status === 'pending' ? 'secondary' : 'destructive'}
                      className="flex-shrink-0"
                    >
                      {doc.status === 'indexed' && <CheckCircle2 className="h-3 w-3 mr-1" />}
                      {doc.status === 'error' && <XCircle className="h-3 w-3 mr-1" />}
                      {doc.status}
                    </Badge>
                    <Button 
                      variant="ghost" 
                      size="icon"
                      onClick={() => handleDelete(doc.id, doc.filename)}
                      className="flex-shrink-0 text-red-600 hover:text-red-700 hover:bg-red-50"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-muted-foreground">
                <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No documents uploaded yet</p>
                <p className="text-sm mt-1">Upload your first medical document to get started</p>
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default AdminDashboard;
