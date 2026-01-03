import { useState, useEffect } from 'react';
import { DashboardLayout } from './Dashboard';
import { api } from '../utils/api';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { GraduationCap, Award, Clock, Star, CheckCircle2 } from 'lucide-react';

function EducationHub() {
  const [lessons, setLessons] = useState([]);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeLevel, setActiveLevel] = useState('all');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [lessonsRes, progressRes] = await Promise.all([
        api.getLessons('all'),
        api.getProgress()
      ]);
      setLessons(lessonsRes.data);
      setProgress(progressRes.data);
    } catch (error) {
      toast.error('Failed to load education data');
    } finally {
      setLoading(false);
    }
  };

  const completeLesson = async (lessonId) => {
    try {
      const response = await api.completeLesson(lessonId);
      setProgress(response.data);
      toast.success('Lesson completed! +100 points');
    } catch (error) {
      toast.error('Failed to complete lesson');
    }
  };

  const filteredLessons = activeLevel === 'all' 
    ? lessons 
    : lessons.filter(l => l.level === activeLevel);

  const levelColors = {
    beginner: 'bg-green-100 text-green-700',
    intermediate: 'bg-yellow-100 text-yellow-700',
    advanced: 'bg-red-100 text-red-700'
  };

  return (
    <DashboardLayout active="/education">
      <div className="p-8">
        <div className="mb-8">
          <h1 data-testid="education-title" className="text-4xl font-semibold text-stone-900 mb-2">
            Education Hub
          </h1>
          <p className="text-lg text-stone-600">Build wealth-building knowledge through interactive learning</p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-stone-500">Loading education hub...</p>
          </div>
        ) : (
          <>
            {/* Progress Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-lime-50 border-2 border-lime-200 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Award className="h-8 w-8 text-lime-600" />
                  <div>
                    <p className="text-sm text-stone-600">Total Points</p>
                    <p className="text-3xl font-semibold text-emerald-900 mono">
                      {progress?.total_points || 0}
                    </p>
                  </div>
                </div>
              </div>
              <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <CheckCircle2 className="h-8 w-8 text-blue-600" />
                  <div>
                    <p className="text-sm text-stone-600">Lessons Completed</p>
                    <p className="text-3xl font-semibold text-blue-900 mono">
                      {progress?.completed_lessons?.length || 0}
                    </p>
                  </div>
                </div>
              </div>
              <div className="bg-purple-50 border-2 border-purple-200 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Star className="h-8 w-8 text-purple-600" />
                  <div>
                    <p className="text-sm text-stone-600">Current Streak</p>
                    <p className="text-3xl font-semibold text-purple-900 mono">
                      {progress?.current_streak || 0} days
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Lessons Section */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <Tabs defaultValue="all" className="w-full">
                <TabsList className="mb-6">
                  <TabsTrigger 
                    data-testid="level-tab-all"
                    value="all" 
                    onClick={() => setActiveLevel('all')}
                  >
                    All Levels
                  </TabsTrigger>
                  <TabsTrigger 
                    data-testid="level-tab-beginner"
                    value="beginner" 
                    onClick={() => setActiveLevel('beginner')}
                  >
                    Beginner
                  </TabsTrigger>
                  <TabsTrigger 
                    data-testid="level-tab-intermediate"
                    value="intermediate" 
                    onClick={() => setActiveLevel('intermediate')}
                  >
                    Intermediate
                  </TabsTrigger>
                  <TabsTrigger 
                    data-testid="level-tab-advanced"
                    value="advanced" 
                    onClick={() => setActiveLevel('advanced')}
                  >
                    Advanced
                  </TabsTrigger>
                </TabsList>

                <TabsContent value={activeLevel} className="space-y-4">
                  {filteredLessons.map((lesson, index) => {
                    const isCompleted = progress?.completed_lessons?.includes(lesson.id);
                    return (
                      <div
                        key={lesson.id}
                        data-testid={`lesson-card-${index}`}
                        className={`border rounded-lg p-5 transition-all ${
                          isCompleted 
                            ? 'border-lime-300 bg-lime-50' 
                            : 'border-stone-200 hover:border-emerald-500 hover:shadow-md'
                        }`}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              <GraduationCap className={`h-6 w-6 ${
                                isCompleted ? 'text-lime-600' : 'text-emerald-600'
                              }`} />
                              <h3 className="text-xl font-semibold text-stone-900">{lesson.title}</h3>
                            </div>
                            <div className="flex items-center gap-3 mb-3">
                              <span className={`px-3 py-1 rounded-full text-xs font-medium ${levelColors[lesson.level]}`}>
                                {lesson.level}
                              </span>
                              <span className="px-3 py-1 bg-stone-100 text-stone-700 text-xs font-medium rounded-full">
                                {lesson.category}
                              </span>
                            </div>
                            <p className="text-stone-600 mb-3">{lesson.content}</p>
                            <div className="flex items-center gap-6 text-sm text-stone-500">
                              <div className="flex items-center gap-2">
                                <Clock className="h-4 w-4" />
                                <span>{lesson.duration_minutes} minutes</span>
                              </div>
                              <div className="flex items-center gap-2">
                                <Award className="h-4 w-4" />
                                <span>{lesson.points} points</span>
                              </div>
                            </div>
                          </div>
                          <div className="ml-4">
                            {isCompleted ? (
                              <div className="flex items-center gap-2 text-lime-600">
                                <CheckCircle2 className="h-6 w-6" />
                                <span className="font-medium">Completed</span>
                              </div>
                            ) : (
                              <Button
                                data-testid={`complete-lesson-btn-${index}`}
                                onClick={() => completeLesson(lesson.id)}
                                className="btn-primary"
                              >
                                Complete
                              </Button>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </TabsContent>
              </Tabs>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}

export default EducationHub;
