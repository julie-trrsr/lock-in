#Perception layer (object/action classifiers)
object_classifier_agent = "Role: Analyzes user's field of view to identify and catalog visible objects"
object_classifier_query = "Input: Image data from user's perspective. Output: {objects: [{type: string,  // e.g. computer, phone, document confidence: float,  // 0-1 detection confidence location: {x,y,w,h},  // bounding box  relevance: float  // 0-1 estimated work relevance}]} Requirements: - Must handle common workplace objects and distractions - Should prioritize objects likely to impact productivity - Needs real-time performance for continuous monitoring"
    
action_classifier_agent = "Role: Identifies current user activities and behaviors"
action_classifier_query = "Input: Image data from user's perspective Output: {    actions: [{        type: string,  // e.g. typing, reading, phone_use  confidence: float, duration: float,  // time spent on action  intensity: float  // 0-1 engagement level    }] } Requirements: - Focus on work vs non-work activities - Track duration and switching between activities - Handle simultaneous/overlapping actions"

#Goal tracking layer (goal/progress classifiers) 
goal_classifier_agent = "Role: Determines if current activities align with user's objectives"
goal_classifier_query = "Input: User's stated goals + Action classifier output Output: {    goal_alignment: float,  // 0-1 alignment score    active_goals: [string],  // relevant goals    obstacles: [string]  // factors impeding progress } Requirements: - Maintain context of user's short/long term goals - Detect goal-aligned vs divergent activities - Consider legitimate breaks/context switches"

progress_classifier_agent = "Role: Evaluates productivity and progress towards goals"
progress_classifier_query = "Input: Goal classifier output + Action classifier output Output: {    progress_score: float,  // 0-1 progress rating    velocity: float,  // rate of progress    bottlenecks: [string],  // progress limiters    momentum: float  // 0-1 sustained progress } Requirements: - Track progress over multiple time scales - Account for different types of productivity - Identify patterns in productive periods"

#Analysis layer (scenario/success classifiers)
senario_classifier_agent = "Role: Synthesizes object and action data into situation understanding"
senario_classifier_query = "Input: Object classifier + Action classifier outputs Output: {    scenario_type: string,  // e.g. 'focused_work', 'distracted'    context: string,  // situational description    risk_factors: [string],  // potential disruptions    opportunity_factors: [string]  // positive elements } Requirements: - Create holistic view of current situation - Identify patterns/trends in scenarios - Consider environmental and behavioral factors"

successful_classifier_agent = "Role: Evaluates overall productivity success based on goals and progress"
successful_classifier_query = "Input: Goal classifier + Progress classifier outputs Output: {    success_score: float,  // 0-1 success rating    key_wins: [string],    key_challenges: [string],    trajectory: string  // 'improving', 'declining', 'stable' } Requirements: - Balance short vs long-term success metrics - Provide granular success decomposition - Identify critical success/failure factors"

#Recommendation layer (distraction improvement)
distraction_improvement_classifier_agent = "Role: Generates actionable recommendations for improving focus"
distraction_improvement_classifier_query = "Input: Scenario classifier + Success classifier outputs Output: {    suggestion: string,  // Single clear recommendation and must be super short and most likely to happen in day to day life    priority: float,  // 0-1 urgency rating    expected_impact: float,  // 0-1 potential benefit    implementation_ease: float  // 0-1 ease of adoption } Requirements: - Provide clear, actionable recommendations - Prioritize high-impact, easy-to-implement changes - Avoid alert fatigue with selective suggestions - Maintain context of previous suggestions"

