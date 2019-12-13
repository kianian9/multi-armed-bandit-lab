# epsilon-greedy example implementation of a multi-armed bandit
import random
from math import fsum, tanh, exp

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import simulator
import reference_bandit

# generic epsilon-greedy bandit
DEFAULT_EPS = 0.9999
class Bandit:
    def __init__(self, arms, epsilon=DEFAULT_EPS):
        self.arms = arms
        self.epsilon = epsilon
        self.frequencies = [0] * len(arms)
        self.sums = [0] * len(arms)
        self.expected_values = [0] * len(arms)
        #self.lastArms =  {'armA':0, 'armB':0, 'armC':0, 'armD':0, 'armE':0}
        #self.lastArm = None
        #self.lastArmCounter = 0
        #self.maxCounter = []


    '''
        def run(self):
        if min(self.frequencies) == 0:
            if self.actualArm is not None and self.actualArm == self.arms[self.frequencies.index(min(self.frequencies))]:
                self.actualArmCounter += 1
            else:
                self.actualArmCounter = 0
            self.actualArm = self.arms[self.frequencies.index(min(self.frequencies))]
            return self.actualArm
        if random.random() < self.epsilon:
            if self.actualArm is not None and self.actualArm == self.arms[random.randint(0, len(arms) - 1)]:
                self.actualArmCounter += 1
            else:
                self.actualArmCounter = 0
            self.actualArm = self.arms[random.randint(0, len(arms) - 1)]
            return self.actualArm
        self.actualArm = self.arms[self.expected_values.index(max(self.expected_values))]
        return self.actualArm
    
    '''

    def run(self):
        if len(self.lastArms) == 50:

        if min(self.frequencies) == 0:
            self.lastArms.append(self.arms[self.frequencies.index(min(self.frequencies))])
            return self.arms[self.frequencies.index(min(self.frequencies))]
        if random.random() < self.epsilon:
            self.lastArms.append(self.arms[random.randint(0, len(arms) - 1)])
            return self.arms[random.randint(0, len(arms) - 1)]
        self.lastArms.append(self.arms[self.expected_values.index(max(self.expected_values))])
        return self.arms[self.expected_values.index(max(self.expected_values))]


    def getBestArm(self):
        armA = 0; armB = 0; armC = 0; armD = 0; armE = 0; armF = 0
        for arm in self.lastArms:





    def give_feedback(self, arm, reward):
        arm_index = self.arms.index(arm)
        sum = self.sums[arm_index] + reward
        self.sums[arm_index] = sum
        frequency = self.frequencies[arm_index] + 1
        self.frequencies[arm_index] = frequency
        expected_value = sum / frequency
        self.expected_values[arm_index] = expected_value



    '''
    def give_feedback(self, arm, reward):
        arm_index = self.arms.index(arm)
        sum = self.sums[arm_index] + reward
        self.sums[arm_index] = sum
        frequency = self.frequencies[arm_index] + 1
        self.frequencies[arm_index] = frequency
        expected_value = sum / frequency
        self.expected_values[arm_index] = expected_value

        self.maxCounter.append(self.actualArmCounter)

        #give feedback by changing epsilon after each 1000 runs
        sumFreq = int(fsum(self.frequencies))
        #print("Actual arm val: " + str(self.actualArmCounter))
        if self.actualArmCounter != 0 and (self.actualArmCounter % 3) == 0:
            #print("arms change")
            self.epsilon -= 0.1
        if (sumFreq % 1000) == 0:
            #print("MAx val is: " + str(max(self.maxCounter)))
            maxVal = max(self.maxCounter)
            newCount = 0
            for maxx in self.maxCounter:
                if maxx == maxVal:
                    newCount += 1
            #print("Epsilon is: " + str(self.epsilon))
            #print("Clears vals")
            #print("got maxval " + str(newCount) + " numbver of times")
            self.clear()



        '''
        #check if one arm has been pulled 50 times in a row

    '''
    sumFreq = int(fsum(self.frequencies))
    if (sumFreq % 50) == 0:
        self.epsilon -= 0.05
    if (sumFreq % 1000) == 0:
        self.clear()
    '''

    def normalizeValue(self, value):
        #normVal = tanh(value)
        #return normVal
        return 1 / (1 + exp(-value))






    '''
    def clear(self):
        print("current eps = " + str(self.epsilon) + ", norm(eps) = " + str(self.normalizeValue(self.epsilon)))
        self.epsilon = DEFAULT_EPS
        self.sums = [0] * len(arms)
        self.expected_values = [0] * len(arms)
        self.actualArmCounter = 0
        self.actualArm = None
        #self.frequencies = [0] * len(arms)
    '''




# configuration
arms = [
    'Configuration a',
    'Configuration b',
    'Configuration c',
    'Configuration d',
    'Configuration e',
    'Configuration f'
]

# instantiate bandits
bandit = Bandit(arms)
ref_bandit = reference_bandit.ReferenceBandit(arms)

