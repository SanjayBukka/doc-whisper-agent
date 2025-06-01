
import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { FileText, Search, BookOpen, CheckCircle, Edit, BarChart3, Zap, Globe, Users, Target, AlertTriangle } from 'lucide-react';
import { useToast } from "@/hooks/use-toast";
import { analyzeDocumentation, type AnalysisResponse } from '@/services/api';

const Index = () => {
  const [url, setUrl] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [analysisResults, setAnalysisResults] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleAnalyze = async () => {
    if (!url) {
      toast({
        title: "URL Required",
        description: "Please enter a documentation URL to analyze.",
        variant: "destructive"
      });
      return;
    }

    setAnalyzing(true);
    setProgress(0);
    setError(null);
    setAnalysisResults(null);

    try {
      // Show progress simulation
      const progressSteps = [
        { name: "Connecting to backend...", duration: 500 },
        { name: "Scraping documentation...", duration: 2000 },
        { name: "Analyzing readability...", duration: 1500 },
        { name: "Evaluating structure...", duration: 1200 },
        { name: "Checking completeness...", duration: 1300 },
        { name: "Analyzing writing style...", duration: 1000 },
        { name: "Generating recommendations...", duration: 800 }
      ];

      // Start the API call
      const analysisPromise = analyzeDocumentation(url);

      // Simulate progress while waiting for API
      for (let i = 0; i < progressSteps.length; i++) {
        setProgress((i + 1) * (100 / progressSteps.length));
        await new Promise(resolve => setTimeout(resolve, progressSteps[i].duration));
      }

      // Wait for the actual API response
      const results = await analysisPromise;
      setAnalysisResults(results);
      
      toast({
        title: "Analysis Complete!",
        description: "Your documentation has been analyzed successfully.",
      });
    } catch (error) {
      console.error('Analysis error:', error);
      setError(error instanceof Error ? error.message : 'An unexpected error occurred');
      toast({
        title: "Analysis Failed",
        description: "Failed to analyze the documentation. Please check the URL and try again.",
        variant: "destructive"
      });
    } finally {
      setAnalyzing(false);
    }
  };

  const testUrls = [
    "https://httpbin.org/html",
    "https://example.com",
    "https://en.wikipedia.org/wiki/Web_scraping"
  ];

  const moengageUrls = [
    "https://partners.moengage.com/hc/en-us/articles/9643917325460-Create-content-creatives",
    "https://help.moengage.com/hc/en-us/articles/28194279371668-How-to-Analyze-OTT-Content-Performance"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 rounded-2xl">
              <BookOpen className="h-12 w-12 text-white" />
            </div>
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            MoEngage Documentation Analyzer
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            AI-powered analysis tool that evaluates documentation articles and provides 
            actionable improvement suggestions for readability, structure, completeness, and writing style.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-4 gap-6 mb-12">
          <Card className="bg-white/70 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardContent className="p-6 text-center">
              <Users className="h-8 w-8 text-blue-600 mx-auto mb-3" />
              <h3 className="font-semibold mb-2">Marketer-Friendly</h3>
              <p className="text-sm text-gray-600">Analyzes readability for non-technical users</p>
            </CardContent>
          </Card>
          
          <Card className="bg-white/70 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardContent className="p-6 text-center">
              <FileText className="h-8 w-8 text-green-600 mx-auto mb-3" />
              <h3 className="font-semibold mb-2">Structure Analysis</h3>
              <p className="text-sm text-gray-600">Evaluates document flow and organization</p>
            </CardContent>
          </Card>
          
          <Card className="bg-white/70 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardContent className="p-6 text-center">
              <CheckCircle className="h-8 w-8 text-purple-600 mx-auto mb-3" />
              <h3 className="font-semibold mb-2">Completeness Check</h3>
              <p className="text-sm text-gray-600">Ensures comprehensive information coverage</p>
            </CardContent>
          </Card>
          
          <Card className="bg-white/70 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardContent className="p-6 text-center">
              <Edit className="h-8 w-8 text-orange-600 mx-auto mb-3" />
              <h3 className="font-semibold mb-2">Style Guidelines</h3>
              <p className="text-sm text-gray-600">Follows Microsoft Style Guide principles</p>
            </CardContent>
          </Card>
        </div>

        {/* Analysis Interface */}
        <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-xl mb-8">
          <CardHeader className="pb-6">
            <CardTitle className="flex items-center gap-3 text-2xl">
              <Search className="h-6 w-6 text-blue-600" />
              Analyze Documentation
            </CardTitle>
            <CardDescription className="text-base">
              Enter a documentation URL to get comprehensive analysis and improvement suggestions.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">
                  Documentation URL
                </label>
                <Input
                  placeholder="https://help.moengage.com/hc/en-us/articles/..."
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="text-base py-3"
                  disabled={analyzing}
                />
              </div>
              
              <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="h-5 w-5 text-orange-600 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-orange-800 mb-2">MoEngage URLs may be blocked</p>
                    <p className="text-sm text-orange-700 mb-3">If you get 403 errors, try these test URLs first:</p>
                    <div className="space-y-2">
                      {testUrls.map((testUrl, index) => (
                        <button
                          key={index}
                          onClick={() => setUrl(testUrl)}
                          className="text-blue-600 hover:text-blue-800 text-sm hover:underline block text-left"
                          disabled={analyzing}
                        >
                          {testUrl}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm font-medium text-gray-700 mb-2">MoEngage URLs (may require alternative access):</p>
                <div className="space-y-2">
                  {moengageUrls.map((exampleUrl, index) => (
                    <button
                      key={index}
                      onClick={() => setUrl(exampleUrl)}
                      className="text-blue-600 hover:text-blue-800 text-sm hover:underline block text-left"
                      disabled={analyzing}
                    >
                      {exampleUrl}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {analyzing && (
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <Zap className="h-5 w-5 text-blue-600 animate-pulse" />
                  <span className="text-sm font-medium">Analyzing documentation...</span>
                </div>
                <Progress value={progress} className="h-2" />
              </div>
            )}

            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <Button 
              onClick={handleAnalyze} 
              disabled={analyzing || !url}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 text-base font-medium"
            >
              {analyzing ? "Analyzing..." : "Analyze Documentation"}
            </Button>
          </CardContent>
        </Card>

        {/* Results Section */}
        {analysisResults && (
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-xl">
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-2xl">
                <BarChart3 className="h-6 w-6 text-green-600" />
                Analysis Results
              </CardTitle>
              <CardDescription>
                Comprehensive analysis of: {analysisResults.document_info.title}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {/* Overview Metrics */}
              <div className="grid md:grid-cols-4 gap-4 mb-8">
                <Card>
                  <CardContent className="p-4 text-center">
                    <div className="text-2xl font-bold text-blue-600">{analysisResults.document_info.word_count}</div>
                    <div className="text-sm text-gray-600">Words</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4 text-center">
                    <div className="text-2xl font-bold text-green-600">{analysisResults.readability.score}</div>
                    <div className="text-sm text-gray-600">Readability Score</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4 text-center">
                    <div className="text-2xl font-bold text-purple-600">{analysisResults.structure.score}</div>
                    <div className="text-sm text-gray-600">Structure Score</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4 text-center">
                    <div className="text-2xl font-bold text-orange-600">{analysisResults.overall_score}</div>
                    <div className="text-sm text-gray-600">Overall Score</div>
                  </CardContent>
                </Card>
              </div>

              {/* Detailed Analysis Tabs */}
              <Tabs defaultValue="readability" className="w-full">
                <TabsList className="grid w-full grid-cols-5">
                  <TabsTrigger value="readability">Readability</TabsTrigger>
                  <TabsTrigger value="structure">Structure</TabsTrigger>
                  <TabsTrigger value="completeness">Completeness</TabsTrigger>
                  <TabsTrigger value="style">Style</TabsTrigger>
                  <TabsTrigger value="summary">Summary</TabsTrigger>
                </TabsList>

                <TabsContent value="readability" className="space-y-6">
                  <Alert>
                    <Target className="h-4 w-4" />
                    <AlertDescription>
                      <strong>Readability Score: {analysisResults.readability.score}/10</strong>
                      <ul className="mt-2 space-y-1">
                        {analysisResults.readability.suggestions.map((suggestion, index) => (
                          <li key={index} className="text-sm">• {suggestion}</li>
                        ))}
                      </ul>
                    </AlertDescription>
                  </Alert>
                </TabsContent>

                <TabsContent value="structure" className="space-y-6">
                  <Alert>
                    <FileText className="h-4 w-4" />
                    <AlertDescription>
                      <strong>Structure Score: {analysisResults.structure.score}/10</strong>
                      <ul className="mt-2 space-y-1">
                        {analysisResults.structure.suggestions.map((suggestion, index) => (
                          <li key={index} className="text-sm">• {suggestion}</li>
                        ))}
                      </ul>
                    </AlertDescription>
                  </Alert>
                </TabsContent>

                <TabsContent value="completeness" className="space-y-6">
                  <Alert>
                    <CheckCircle className="h-4 w-4" />
                    <AlertDescription>
                      <strong>Completeness Score: {analysisResults.completeness.score}/10</strong>
                      <ul className="mt-2 space-y-1">
                        {analysisResults.completeness.suggestions.map((suggestion, index) => (
                          <li key={index} className="text-sm">• {suggestion}</li>
                        ))}
                      </ul>
                    </AlertDescription>
                  </Alert>
                </TabsContent>

                <TabsContent value="style" className="space-y-6">
                  <Alert>
                    <Edit className="h-4 w-4" />
                    <AlertDescription>
                      <strong>Style Score: {analysisResults.style.score}/10</strong>
                      <ul className="mt-2 space-y-1">
                        {analysisResults.style.suggestions.map((suggestion, index) => (
                          <li key={index} className="text-sm">• {suggestion}</li>
                        ))}
                      </ul>
                    </AlertDescription>
                  </Alert>
                </TabsContent>

                <TabsContent value="summary" className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <Card>
                      <CardHeader>
                        <CardTitle className="text-lg text-green-600">Strengths</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <ul className="space-y-1">
                          {analysisResults.summary.strengths.map((strength, index) => (
                            <li key={index} className="text-sm">• {strength}</li>
                          ))}
                        </ul>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardHeader>
                        <CardTitle className="text-lg text-red-600">Areas for Improvement</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <ul className="space-y-1">
                          {analysisResults.summary.priority_improvements.map((improvement, index) => (
                            <li key={index} className="text-sm">• {improvement}</li>
                          ))}
                        </ul>
                      </CardContent>
                    </Card>
                  </div>
                  
                  <Alert>
                    <AlertDescription>
                      <strong>Recommendation:</strong> {analysisResults.summary.recommendation}
                    </AlertDescription>
                  </Alert>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        )}

        {/* Footer */}
        <div className="text-center mt-16 py-8 border-t border-gray-200">
          <p className="text-gray-600">
            Built with React, TypeScript, and Python • 
            <span className="ml-2">Powered by AI for intelligent documentation analysis</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Index;
