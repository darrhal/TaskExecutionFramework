"""
Self-Improvement Mechanisms for TEF
Phase 6.3: Learning from execution, pattern recognition, and instruction refinement
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, Counter
import statistics


class PatternRecognizer:
    """Recognizes patterns in execution history for learning."""
    
    def __init__(self, state_dir: str = "state"):
        self.state_dir = Path(state_dir)
        self.patterns_file = self.state_dir / "execution_patterns.json"
        self.learning_file = self.state_dir / "learning_insights.json"
        
    def analyze_execution_patterns(self, execution_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in execution history."""
        if not execution_history:
            return {"patterns": [], "insights": [], "recommendations": []}
        
        patterns = {
            "success_patterns": self._analyze_success_patterns(execution_history),
            "failure_patterns": self._analyze_failure_patterns(execution_history),
            "performance_patterns": self._analyze_performance_patterns(execution_history),
            "decision_patterns": self._analyze_decision_patterns(execution_history),
            "temporal_patterns": self._analyze_temporal_patterns(execution_history)
        }
        
        insights = self._generate_insights(patterns)
        recommendations = self._generate_recommendations(patterns, insights)
        
        result = {
            "analysis_timestamp": datetime.now().isoformat(),
            "executions_analyzed": len(execution_history),
            "patterns": patterns,
            "insights": insights,
            "recommendations": recommendations
        }
        
        # Save patterns for future reference
        self._save_patterns(result)
        
        return result
    
    def _analyze_success_patterns(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in successful executions."""
        successful = [h for h in history if h.get("status") == "success"]
        
        if not successful:
            return {"count": 0, "patterns": []}
        
        # Analyze common factors in successful executions
        task_types = Counter(h.get("orchestrator_metadata", {}).get("task_type") for h in successful)
        execution_times = [h.get("orchestrator_metadata", {}).get("execution_time", 0) for h in successful]
        depths = Counter(h.get("orchestrator_metadata", {}).get("depth", 0) for h in successful)
        
        return {
            "count": len(successful),
            "task_type_distribution": dict(task_types),
            "avg_execution_time": statistics.mean(execution_times) if execution_times else 0,
            "depth_distribution": dict(depths),
            "success_rate": len(successful) / len(history),
            "patterns": [
                {
                    "pattern": "fast_execution",
                    "condition": "execution_time < 1.0",
                    "frequency": len([t for t in execution_times if t < 1.0]) / len(execution_times) if execution_times else 0
                }
            ]
        }
    
    def _analyze_failure_patterns(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in failed executions."""
        failed = [h for h in history if h.get("status") in ["failure", "error"]]
        
        if not failed:
            return {"count": 0, "patterns": []}
        
        # Analyze common failure causes
        error_types = Counter()
        failure_phases = Counter()
        retry_counts = Counter()
        
        for failure in failed:
            error = failure.get("error", "unknown")
            error_types[self._categorize_error(error)] += 1
            
            if "recovery_info" in failure:
                failure_phases[failure["recovery_info"].get("phase", "unknown")] += 1
                retry_counts[failure["recovery_info"].get("failure_count", 0)] += 1
        
        return {
            "count": len(failed),
            "failure_rate": len(failed) / len(history),
            "error_categories": dict(error_types),
            "failure_phases": dict(failure_phases),
            "retry_distribution": dict(retry_counts),
            "patterns": [
                {
                    "pattern": "communication_file_errors",
                    "frequency": error_types.get("file_access", 0) / len(failed) if failed else 0,
                    "recommendation": "Ensure communication files are initialized"
                }
            ]
        }
    
    def _analyze_performance_patterns(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance patterns."""
        execution_times = []
        for h in history:
            exec_time = h.get("orchestrator_metadata", {}).get("execution_time")
            if exec_time is not None:
                execution_times.append(exec_time)
        
        if not execution_times:
            return {"patterns": []}
        
        return {
            "avg_execution_time": statistics.mean(execution_times),
            "median_execution_time": statistics.median(execution_times),
            "max_execution_time": max(execution_times),
            "min_execution_time": min(execution_times),
            "patterns": [
                {
                    "pattern": "performance_degradation",
                    "detected": max(execution_times) > statistics.mean(execution_times) * 3,
                    "threshold": statistics.mean(execution_times) * 3
                }
            ]
        }
    
    def _analyze_decision_patterns(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze decision-making patterns."""
        # This would analyze navigator decisions from plan_updates.json
        # For now, return basic structure
        return {
            "patterns": [
                {
                    "pattern": "retry_preference",
                    "description": "System tends to retry failed tasks",
                    "frequency": 0.8  # Would calculate from actual data
                }
            ]
        }
    
    def _analyze_temporal_patterns(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze temporal execution patterns."""
        timestamps = []
        for h in history:
            try:
                timestamp = datetime.fromisoformat(h.get("timestamp", ""))
                timestamps.append(timestamp)
            except:
                continue
        
        if len(timestamps) < 2:
            return {"patterns": []}
        
        # Analyze execution intervals
        intervals = []
        for i in range(1, len(timestamps)):
            interval = (timestamps[i] - timestamps[i-1]).total_seconds()
            intervals.append(interval)
        
        return {
            "avg_interval": statistics.mean(intervals) if intervals else 0,
            "patterns": [
                {
                    "pattern": "execution_frequency",
                    "avg_seconds_between_executions": statistics.mean(intervals) if intervals else 0
                }
            ]
        }
    
    def _categorize_error(self, error_message: str) -> str:
        """Categorize error message into error type."""
        error_lower = error_message.lower()
        
        if "no such file" in error_lower or "file not found" in error_lower:
            return "file_access"
        elif "timeout" in error_lower:
            return "timeout"
        elif "permission" in error_lower:
            return "permission"
        elif "connection" in error_lower:
            return "network"
        else:
            return "unknown"
    
    def _generate_insights(self, patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate insights from patterns."""
        insights = []
        
        # Success rate insight
        success_patterns = patterns.get("success_patterns", {})
        failure_patterns = patterns.get("failure_patterns", {})
        
        if success_patterns.get("success_rate", 0) < 0.5:
            insights.append({
                "type": "performance",
                "level": "warning",
                "message": f"Low success rate: {success_patterns.get('success_rate', 0):.2%}",
                "recommendation": "Review task specifications and error handling"
            })
        
        # Failure pattern insight
        if failure_patterns.get("count", 0) > 0:
            top_error = max(failure_patterns.get("error_categories", {}), 
                          key=failure_patterns.get("error_categories", {}).get, default="none")
            if top_error != "none":
                insights.append({
                    "type": "reliability",
                    "level": "info",
                    "message": f"Most common error type: {top_error}",
                    "recommendation": f"Focus on improving {top_error} handling"
                })
        
        return insights
    
    def _generate_recommendations(self, patterns: Dict[str, Any], insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations."""
        recommendations = []
        
        failure_patterns = patterns.get("failure_patterns", {})
        
        # File access error recommendation
        if failure_patterns.get("error_categories", {}).get("file_access", 0) > 0:
            recommendations.append({
                "priority": "high",
                "category": "system",
                "action": "initialize_communication_files",
                "description": "Initialize agent communication files before execution",
                "implementation": "Add communication hub initialization to orchestrator startup"
            })
        
        # Performance recommendation
        performance_patterns = patterns.get("performance_patterns", {})
        if performance_patterns.get("avg_execution_time", 0) > 5.0:
            recommendations.append({
                "priority": "medium",
                "category": "performance",
                "action": "optimize_execution",
                "description": "Consider optimizing task execution paths",
                "implementation": "Review timeout settings and agent efficiency"
            })
        
        return recommendations
    
    def _save_patterns(self, analysis_result: Dict[str, Any]) -> None:
        """Save pattern analysis results."""
        try:
            # Load existing patterns
            existing_patterns = []
            if self.patterns_file.exists():
                with open(self.patterns_file, 'r') as f:
                    data = json.load(f)
                    existing_patterns = data.get("analyses", [])
            
            # Add new analysis
            existing_patterns.append(analysis_result)
            
            # Keep only last 10 analyses
            if len(existing_patterns) > 10:
                existing_patterns = existing_patterns[-10:]
            
            # Save updated patterns
            with open(self.patterns_file, 'w') as f:
                json.dump({
                    "last_updated": datetime.now().isoformat(),
                    "analyses": existing_patterns
                }, f, indent=2)
                
        except Exception as e:
            print(f"[LEARNING] Error saving patterns: {e}")


class InstructionRefinement:
    """Refines agent instructions based on learning."""
    
    def __init__(self, agents_dir: str = "agents", state_dir: str = "state"):
        self.agents_dir = Path(agents_dir)
        self.state_dir = Path(state_dir)
        self.refinements_file = self.state_dir / "instruction_refinements.json"
    
    def refine_instructions(self, pattern_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Refine agent instructions based on pattern analysis."""
        refinements = {
            "timestamp": datetime.now().isoformat(),
            "analysis_based_on": pattern_analysis.get("analysis_timestamp"),
            "refinements": []
        }
        
        # Generate instruction refinements based on patterns
        recommendations = pattern_analysis.get("recommendations", [])
        
        for rec in recommendations:
            if rec.get("category") == "system":
                refinement = self._create_system_refinement(rec)
                if refinement:
                    refinements["refinements"].append(refinement)
        
        # Save refinements
        self._save_refinements(refinements)
        
        return refinements
    
    def _create_system_refinement(self, recommendation: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create system-level instruction refinement."""
        if recommendation.get("action") == "initialize_communication_files":
            return {
                "agent": "executor_agent",
                "refinement_type": "initialization",
                "description": "Add communication file initialization check",
                "instruction_addition": (
                    "Before executing any task, verify that agent communication files exist. "
                    "If agent_messages.json, shared_context.json, or knowledge_base.json are missing, "
                    "initialize them with empty structures to prevent file access errors."
                ),
                "priority": "high",
                "implementation_status": "pending"
            }
        
        return None
    
    def _save_refinements(self, refinements: Dict[str, Any]) -> None:
        """Save instruction refinements."""
        try:
            with open(self.refinements_file, 'w') as f:
                json.dump(refinements, f, indent=2)
        except Exception as e:
            print(f"[LEARNING] Error saving refinements: {e}")


class SelfImprovementEngine:
    """Main self-improvement engine that coordinates learning."""
    
    def __init__(self, state_dir: str = "state", agents_dir: str = "agents"):
        self.state_dir = Path(state_dir)
        self.pattern_recognizer = PatternRecognizer(state_dir)
        self.instruction_refiner = InstructionRefinement(agents_dir, state_dir)
        
    def perform_self_improvement(self, execution_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform complete self-improvement cycle."""
        improvement_cycle = {
            "started_at": datetime.now().isoformat(),
            "executions_analyzed": len(execution_history)
        }
        
        try:
            # Step 1: Analyze patterns
            print(f"[LEARNING] Analyzing {len(execution_history)} execution records")
            pattern_analysis = self.pattern_recognizer.analyze_execution_patterns(execution_history)
            improvement_cycle["pattern_analysis"] = pattern_analysis
            
            # Step 2: Refine instructions
            print(f"[LEARNING] Generating instruction refinements")
            refinements = self.instruction_refiner.refine_instructions(pattern_analysis)
            improvement_cycle["instruction_refinements"] = refinements
            
            # Step 3: Generate learning summary
            improvement_cycle["learning_summary"] = self._generate_learning_summary(
                pattern_analysis, refinements
            )
            
            improvement_cycle["status"] = "completed"
            
        except Exception as e:
            improvement_cycle["status"] = "failed"
            improvement_cycle["error"] = str(e)
            print(f"[LEARNING] Self-improvement cycle failed: {e}")
        
        improvement_cycle["completed_at"] = datetime.now().isoformat()
        
        # Save improvement cycle results
        self._save_improvement_cycle(improvement_cycle)
        
        return improvement_cycle
    
    def _generate_learning_summary(self, patterns: Dict[str, Any], refinements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of what was learned."""
        insights = patterns.get("insights", [])
        recommendations = patterns.get("recommendations", [])
        
        return {
            "key_insights": len(insights),
            "recommendations_generated": len(recommendations),
            "instruction_refinements": len(refinements.get("refinements", [])),
            "top_insight": insights[0]["message"] if insights else "No insights generated",
            "improvement_opportunities": [rec["description"] for rec in recommendations]
        }
    
    def _save_improvement_cycle(self, cycle_result: Dict[str, Any]) -> None:
        """Save improvement cycle results."""
        try:
            cycles_file = self.state_dir / "improvement_cycles.json"
            
            # Load existing cycles
            existing_cycles = []
            if cycles_file.exists():
                with open(cycles_file, 'r') as f:
                    data = json.load(f)
                    existing_cycles = data.get("cycles", [])
            
            # Add new cycle
            existing_cycles.append(cycle_result)
            
            # Keep only last 5 cycles
            if len(existing_cycles) > 5:
                existing_cycles = existing_cycles[-5:]
            
            # Save updated cycles
            with open(cycles_file, 'w') as f:
                json.dump({
                    "last_updated": datetime.now().isoformat(),
                    "cycles": existing_cycles
                }, f, indent=2)
                
        except Exception as e:
            print(f"[LEARNING] Error saving improvement cycle: {e}")


# Integration function
def run_self_improvement_cycle(state_dir: str = "state") -> Dict[str, Any]:
    """Run a complete self-improvement cycle."""
    try:
        # Load execution history
        history_file = Path(state_dir) / "execution_history.json"
        if not history_file.exists():
            return {"status": "skipped", "reason": "No execution history found"}
        
        with open(history_file, 'r') as f:
            data = json.load(f)
            execution_history = data.get("executions", [])
        
        # Run improvement cycle
        engine = SelfImprovementEngine(state_dir)
        return engine.perform_self_improvement(execution_history)
        
    except Exception as e:
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    # Example usage
    result = run_self_improvement_cycle()
    print(f"Self-improvement cycle result: {result.get('status')}")
    print(f"Learning summary: {result.get('learning_summary', {})}")