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
EPS_EXPLOIT_RATE = 0.98
EPS_EXPLORE_RATE = 1.02
BAD_REWARD_RATE = 0.8
CHECK_SIZE = 50
EXPECTED_DECREASE_RATE = 0.05
EXPECTED_INCREASE_RATE = 0.25
#EXPECTED_DECREASE_RATE = 10
#EXPECTED_INCREASE_RATE = 10

class Bandit:
    def __init__(self, arms, epsilon=DEFAULT_EPS):
        self.arms = arms
        self.epsilon = epsilon
        self.frequencies = [0] * len(arms)
        self.sums = [0] * len(arms)
        self.expected_values = [0] * len(arms)
        #self.lastArms = []
        self.lastArmRewards = []
        self.armHistory = [[],[],[],[],[],[]]
        self.counter = 0


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


    #add all reward values to each arm
        #updateHistory()


    #check the last 50 values for an arm and determine the trend



    #if bad trend avoid the arm and choose the best one





    def run(self):
        if min(self.frequencies) == 0:
            return self.arms[self.frequencies.index(min(self.frequencies))]
        if random.random() < self.epsilon:
            #print("Counter: " + str(self.counter))
            #self.counter += 1
            index = random.randint(0, len(arms) - 1)
            index = self.getBestArm(index)
            return self.arms[index]
        return self.arms[self.expected_values.index(max(self.expected_values))]


    '''
    def getBestArm(self, armIndex):
        armIndexList = [0, 1, 2, 3, 4, 5]
        armWasGood = self.checkBestArm(self.armHistory[armIndex])
        lowestBadRewards = -1
        bestArmIndex = armIndex
        if armWasGood is not None:
            return armIndex
        else:
            for index in armIndexList:
                if index == armIndex:
                    continue
                else:
                    badRewards = self.checkBestArm(self.armHistory[index])
                    if badRewards is not None and lowestBadRewards < badRewards:
                        lowestBadRewards = badRewards
                        bestArmIndex = index

        return bestArmIndex
    '''

    def getBestArm(self, armIndex):
        armIndexList = [0, 1, 2, 3, 4, 5]
        nrBadRewards = CHECK_SIZE
        bestArmIndex = armIndex
        if len(self.armHistory[armIndex]) >= CHECK_SIZE:
            wasBadTrend, rewardVal = self.lastRewardsGettingBad(self.armHistory[armIndex])
            if not wasBadTrend:
                return armIndex
        for index in armIndexList:
            if index == armIndex:
                continue
            else:
                if len(self.armHistory[index]) >= CHECK_SIZE:
                    wasBadTrend, rewardVal = self.lastRewardsGettingBad(self.armHistory[index])
                    if not wasBadTrend:
                        if rewardVal < nrBadRewards:
                            nrBadRewards = rewardVal
                            bestArmIndex = index
        return bestArmIndex








    '''
    def checkBestArm(self, checkList):
        badRewardsCounter = 0
        listLen = len(checkList)
        if listLen >= 50:
            if (listLen % 50) == 0:
                lastRewardsList = checkList[listLen - 50: listLen]
                actualRew = lastRewardsList[0]
                for i in range(0,len(lastRewardsList)):
                    nextReward = lastRewardsList[i]
                    if actualRew >= nextReward:
                        badRewardsCounter += 1
                    actualRew = nextReward
                if badRewardsCounter < (50 * 0.25):
                    return badRewardsCounter
            return None
        else:
            return badRewardsCounter
    '''
    # Ger average reward
    def getAverageReward(self, checkList):
        totalRewardScore = 0
        listLen = len(checkList)
        if listLen >= CHECK_SIZE:
            if (listLen % CHECK_SIZE) == 0:
                lastRewardsList = checkList[listLen - CHECK_SIZE: listLen]
                for rew in lastRewardsList:
                    totalRewardScore += rew
                return totalRewardScore/CHECK_SIZE
        return None



    def lastRewardsGettingBad(self, checkList):
        listLen = len(checkList)
        badRewardsCounter = 0
        if (listLen % CHECK_SIZE) == 0:
            lastRewardsList = checkList[listLen - CHECK_SIZE: listLen]
            actualRew = lastRewardsList[0]
            for i in range(1, len(lastRewardsList)):
                #print("rewardlist")
                #print("index=" + str(i) + ", " + str(lastRewardsList[i]) + "\n\n\n")
                nextReward = lastRewardsList[i]
                if actualRew > nextReward:
                    badRewardsCounter += 1
                actualRew = nextReward
                #print(badRewardsCounter)
            #print(badRewardsCounter)
            truthval = (badRewardsCounter >= CHECK_SIZE * BAD_REWARD_RATE)
            #print("Ska returna " + str(badRewardsCounter) + ", truthvalue=" + str(truthval))
            return (badRewardsCounter >= CHECK_SIZE * BAD_REWARD_RATE), badRewardsCounter
        return None, CHECK_SIZE




    def give_feedback(self, arm, reward):
        #if len(self.lastArms) < 50:
        #    self.lastArms.append(arm)

        arm_index = self.arms.index(arm)
        sum = self.sums[arm_index] + reward
        self.sums[arm_index] = sum
        frequency = self.frequencies[arm_index] + 1
        self.frequencies[arm_index] = frequency
        expected_value = sum / frequency
        self.expected_values[arm_index] = expected_value

        #self.lastArms.append(arm)
        self.lastArmRewards.append(reward)

        self.armHistory[arm_index].append(reward)

        if len(self.lastArmRewards) >= CHECK_SIZE:
            wasBadTrend, rewardVal = self.lastRewardsGettingBad(self.lastArmRewards)
            if wasBadTrend:
                self.expected_values[arm_index] -= EXPECTED_DECREASE_RATE
                if 0 < (self.epsilon * EPS_EXPLORE_RATE) < 1:
                    self.epsilon *= EPS_EXPLORE_RATE

            else:
                self.expected_values[arm_index] += EXPECTED_INCREASE_RATE
                if 0 < (self.epsilon * EPS_EXPLOIT_RATE) < 1:
                    self.epsilon *= EPS_EXPLOIT_RATE

        #print(self.epsilon)

        '''
        if self.lastArmRewards[len(self.lastArmRewards) - 1] < reward:
            #print("IF")
            self.expected_values[arm_index] -= 0.1
            #print(self.expected_values[arm_index])
        else:
            #print("ELSE")
            self.expected_values[arm_index] += 0.3
            self.epsilon = self.normalizeValue(self.epsilon - 0.1)
        '''
        #print(self.expected_values[arm_index])
        #print(self.epsilon)



        #if len(self.lastArmRewards) > 50:
        #    del self.lastArmRewards[50]
        #    if fsum(self.lastArmRewards) > 0:
        #        print(fsum(self.lastArmRewards))
        #    else:
        #        print(fsum(self.lastArmRewards))








        '''
        arm_index = self.arms.index(arm)
        sum = self.sums[arm_index] + reward
        self.sums[arm_index] = sum
        frequency = self.frequencies[arm_index] + 1
        self.frequencies[arm_index] = frequency
        expected_value = sum / frequency
        self.expected_values[arm_index] = expected_value
        '''



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

