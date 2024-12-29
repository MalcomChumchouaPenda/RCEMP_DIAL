
import numpy as np
from benchmarks.schema import MaintenanceTask
from ..base import BasicModel
from .agents import RegulatorAgent
from .env import Env


class RCEMPModel(BasicModel):

    def __init__(self, db_id, benchmark_id, problem_id, verbose=None, seed=None):
        super().__init__(db_id, benchmark_id, problem_id, verbose=verbose, seed=seed)
        self.env = Env(self)
        
        problem = self.experiment.problem
        regulator = RegulatorAgent('r0', self, problem)
        self.schedule.add(regulator)
        self.regulator = regulator
    
    @property
    def satisfaction(self):
        return self.regulator.satisfied

    @property
    def cycle_number(self):
        return self.schedule.steps

    @property
    def maintenance_number(self):
        return len([obj for obj in self.env.values() 
                        if isinstance(obj.task, MaintenanceTask)])

    @property
    def late_job_number(self):
        customers = self.regulator.customers
        return len([c for c in customers
                        if c.completion_date > c.due_date])
        
    @property
    def total_tardiness(self):
        customers = self.regulator.customers
        return sum([max(0, c.completion_date - c.due_date) 
                        for c in customers])

    @property
    def max_completion_time(self):
        customers = self.regulator.customers
        return max([c.completion_date for c in customers])
        
    @property
    def unavailability(self):
        producers = self.producers
        return np.product([p.unavailability for p in producers])
