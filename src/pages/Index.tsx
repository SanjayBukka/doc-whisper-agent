
import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Separator } from "@/components/ui/separator";
import { FileText, Search, BookOpen, CheckCircle, Edit, BarChart3, Zap, Globe, Users, Target } from 'lucide-react';
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [url, setUrl] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [analysisResults, setAnalysisResults] = useState(null);
  const { toast } = useToast();

  const handleAnalyze = async () => {
    if (!url) {
      toast({
        title: "URL Required",
        description: "Please enter a MoEngage documentation URL to analyze.",
        variant: "destructive"
      });
      return;
    }

    setAnalyzing(true);
    setProgress(0);

    // Simulate analysis process
    const steps = [
      { name: "Scraping documentation...", duration: 1000 },
      { name: "Analyzing readability...", duration: 1500 },
      { name: "Evaluating structure...", duration: 1200 },
      { name: "Checking completeness...", duration: 1300 },
      { name: "Analyzing writing style...", duration: 1000 },
      { name: "Generating recommendations...", duration: 800 }
    ];

    for (let i = 0; i < steps.length; i++) {
      setProgress((i + 1) * (100 / steps.length));
      await new Promise(resolve => setTimeout(resolve, steps[i].duration));
    }

    // Simulate analysis results
    const mockResults = {
      url: url,
      title: "Creating and Managing User Segments in MoEngage",
      wordCount: 1247,
      headingCount: 8,
      imageCount: 5,
      readability: {
        fleschScore: 52.3,
        gradeLevel: 10.2,
        level: "Fairly Difficult",
        suggestions: [
          "Average sentence length is 22.4 words. Consider breaking long sentences into shorter ones (aim for 15-20 words).",
          "Text contains technical jargon that may be difficult for marketers. Consider adding definitions or simpler explanations.",
          "Some paragraphs exceed 100 words. Break them into smaller, focused paragraphs."
        ]
      },
      structure: {
        headingLevels: [1, 2, 3],
        hasGaps: false,
        avgParagraphLength: 87,
        suggestions: [
          "Good heading hierarchy maintained throughout the document.",
          "Consider adding more subheadings to break up longer sections.",
          "Some sections could benefit from bullet points or numbered lists for better scannability."
        ]
      },
      completeness: {
        hasExamples: true,
        exampleCount: 3,
        hasSteps: true,
        hasCodeBlocks: true,
        suggestions: [
          "Examples are present but could be more diverse to cover different use cases.",
          "Consider adding a troubleshooting section for common issues.",
          "Prerequisites section could be more detailed for new users."
        ]
      },
      style: {
        passiveVoiceRatio: 0.28,
        actionLanguageRatio: 0.12,
        consistencyScore: 78,
        suggestions: [
          "High passive voice usage (28%). Use active voice for clearer instructions.",
          "Add more action-oriented language with clear imperatives (e.g., 'Click here', 'Enter your data').",
          "Tone is professional but could be more customer-focused in some sections."
        ]
      },
      overallScore: 73
    };

    setAnalysisResults(mockResults);
    setAnalyzing(false);
    
    toast({
      title: "Analysis Complete!",
      description: "Your documentation has been analyzed successfully.",
    });
  };

  const exampleUrls = [
    "https://help.moengage.com/hc/en-us/articles/4404464738196-Creating-and-Managing-Segments",
    "https://help.moengage.com/hc/en-us/articles/4404464738324-Setting-up-Push-Notifications",
    "https://help.moengage.com/hc/en-us/articles/4404464738452-Email-Campaign-Setup"
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
            AI-powered analysis tool that evaluates MoEngage documentation articles and provides 
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
              Enter a MoEngage documentation URL to get comprehensive analysis and improvement suggestions.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">
                  MoEngage Documentation URL
                </label>
                <Input
                  placeholder="https://help.moengage.com/hc/en-us/articles/..."
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="text-base py-3"
                  disabled={analyzing}
                />
              </div>
              
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm font-medium text-gray-700 mb-2">Example URLs:</p>
                <div className="space-y-2">
                  {exampleUrls.map((exampleUrl, index) => (
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
                Comprehensive analysis of: {analysisResults.title}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {/* Overview Metrics */}
              <div className="grid md:grid-cols-4 gap-4 mb-8">
                <Card>
                  <CardContent className="p-4 text-center">
                    <div className="text-2xl font-bold text-blue-600">{analysisResults.wordCount}</div>
                    <div className="text-sm text-gray-600">Words</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4 text-center">
                    <div className="text-2xl font-bold text-green-600">{analysisResults.headingCount}</div>
                    <div className="text-sm text-gray-600">Headings</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4 text-center">
                    <div className="text-2xl font-bold text-purple-600">{analysisResults.imageCount}</div>
                    <div className="text-sm text-gray-600">Images</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4 text-center">
                    <div className="text-2xl font-bold text-orange-600">{analysisResults.overallScore}</div>
                    <div className="text-sm text-gray-600">Overall Score</div>
                  </CardContent>
                </Card>
              </div>

              {/* Detailed Analysis Tabs */}
              <Tabs defaultValue="readability" className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="readability">Readability</TabsTrigger>
                  <TabsTrigger value="structure">Structure</TabsTrigger>
                  <TabsTrigger value="completeness">Completeness</TabsTrigger>
                  <TabsTrigger value="style">Style</TabsTrigger>
                </TabsList>

                <TabsContent value="readability" className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-4">
                    <Card>
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-blue-600">{analysisResults.readability.fleschScore}</div>
                        <div className="text-sm text-gray-600">Flesch Score</div>
                        <Badge variant="secondary" className="mt-2">{analysisResults.readability.level}</Badge>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-green-600">{analysisResults.readability.gradeLevel}</div>
                        <div className="text-sm text-gray-600">Grade Level</div>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardContent className="p-4 text-center">
                        <Progress value={analysisResults.readability.fleschScore} className="mb-2" />
                        <div className="text-sm text-gray-600">Readability Progress</div>
                      </CardContent>
                    </Card>
                  </div>
                  
                  <Alert>
                    <Target className="h-4 w-4" />
                    <AlertDescription>
                      <strong>Suggestions for Improvement:</strong>
                      <ul className="mt-2 space-y-1">
                        {analysisResults.readability.suggestions.map((suggestion, index) => (
                          <li key={index} className="text-sm">• {suggestion}</li>
                        ))}
                      </ul>
                    </AlertDescription>
                  </Alert>
                </TabsContent>

                <TabsContent value="structure" className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-4">
                    <Card>
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-purple-600">{analysisResults.structure.headingLevels.length}</div>
                        <div className="text-sm text-gray-600">Heading Levels</div>
                        <div className="text-xs text-gray-500 mt-1">H{analysisResults.structure.headingLevels.join(', H')}</div>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-orange-600">{analysisResults.structure.avgParagraphLength}</div>
                        <div className="text-sm text-gray-600">Avg Paragraph Length</div>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardContent className="p-4 text-center">
                        <Badge variant={analysisResults.structure.hasGaps ? "destructive" : "default"}>
                          {analysisResults.structure.hasGaps ? "Has Gaps" : "Well Structured"}
                        </Badge>
                        <div className="text-sm text-gray-600 mt-2">Hierarchy Status</div>
                      </CardContent>
                    </Card>
                  </div>

                  <Alert>
                    <FileText className="h-4 w-4" />
                    <AlertDescription>
                      <strong>Structure Recommendations:</strong>
                      <ul className="mt-2 space-y-1">
                        {analysisResults.structure.suggestions.map((suggestion, index) => (
                          <li key={index} className="text-sm">• {suggestion}</li>
                        ))}
                      </ul>
                    </AlertDescription>
                  </Alert>
                </TabsContent>

                <TabsContent value="completeness" className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-4">
                    <Card>
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-green-600">{analysisResults.completeness.exampleCount}</div>
                        <div className="text-sm text-gray-600">Examples</div>
                        <Badge variant={analysisResults.completeness.hasExamples ? "default" : "destructive"} className="mt-2">
                          {analysisResults.completeness.hasExamples ? "Present" : "Missing"}
                        </Badge>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardContent className="p-4 text-center">
                        <Badge variant={analysisResults.completeness.hasSteps ? "default" : "destructive"}>
                          {analysisResults.completeness.hasSteps ? "Has Steps" : "No Steps"}
                        </Badge>
                        <div className="text-sm text-gray-600 mt-2">Step-by-Step Guide</div>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardContent className="p-4 text-center">
                        <Badge variant={analysisResults.completeness.hasCodeBlocks ? "default" : "secondary"}>
                          {analysisResults.completeness.hasCodeBlocks ? "Code Present" : "No Code"}
                        </Badge>
                        <div className="text-sm text-gray-600 mt-2">Code Examples</div>
                      </CardContent>
                    </Card>
                  </div>

                  <Alert>
                    <CheckCircle className="h-4 w-4" />
                    <AlertDescription>
                      <strong>Completeness Improvements:</strong>
                      <ul className="mt-2 space-y-1">
                        {analysisResults.completeness.suggestions.map((suggestion, index) => (
                          <li key={index} className="text-sm">• {suggestion}</li>
                        ))}
                      </ul>
                    </AlertDescription>
                  </Alert>
                </TabsContent>

                <TabsContent value="style" className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-4">
                    <Card>
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-red-600">{Math.round(analysisResults.style.passiveVoiceRatio * 100)}%</div>
                        <div className="text-sm text-gray-600">Passive Voice</div>
                        <Badge variant="destructive" className="mt-2">Too High</Badge>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-orange-600">{Math.round(analysisResults.style.actionLanguageRatio * 100)}%</div>
                        <div className="text-sm text-gray-600">Action Language</div>
                        <Badge variant="secondary" className="mt-2">Needs Improvement</Badge>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-blue-600">{analysisResults.style.consistencyScore}</div>
                        <div className="text-sm text-gray-600">Consistency Score</div>
                        <Progress value={analysisResults.style.consistencyScore} className="mt-2" />
                      </CardContent>
                    </Card>
                  </div>

                  <Alert>
                    <Edit className="h-4 w-4" />
                    <AlertDescription>
                      <strong>Style Enhancements:</strong>
                      <ul className="mt-2 space-y-1">
                        {analysisResults.style.suggestions.map((suggestion, index) => (
                          <li key={index} className="text-sm">• {suggestion}</li>
                        ))}
                      </ul>
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
            Built with React, TypeScript, and Tailwind CSS • 
            <span className="ml-2">Powered by AI for intelligent documentation analysis</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Index;
