# epsilon-greedy example implementation of a multi-armed bandit
import random

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import simulator
import reference_bandit

# generic epsilon-greedy bandit
DEFAULT_EPS = 0.5
BAD_REWARD_RATE = 0.8
CHECK_SIZE = 5
EXPECTED_DECREASE_RATE = 1
EXPECTED_INCREASE_RATE = 1

class Bandit:
    def __init__(self, arms, epsilon=DEFAULT_EPS):
        self.arms = arms
        self.epsilon = epsilon
        self.frequencies = [0] * len(arms)
        self.sums = [0] * len(arms)
        self.expected_values = [0] * len(arms)
        self.armHistory = [[],[],[],[],[],[]]


    def run(self):
        ''' Chooses the bandit arm depending on the AI should explore or exploit '''
        if min(self.frequencies) == 0:
            return self.arms[self.frequencies.index(min(self.frequencies))]
        if random.random() < self.epsilon:
            index = random.randint(0, len(arms) - 1)
            index = self.getBestArm(index)
            return self.arms[index]
        return self.arms[self.expected_values.index(max(self.expected_values))]

    def getBestArm(self, armIndex):
        '''
            Gets the best arm if the generated arm-index didn't correspond to
            to a reward history list that didn't have any negative trend
        '''
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
                if len(self.armHistory[index]) >= CHECK_SIZE :
                    wasBadTrend, rewardVal = self.lastRewardsGettingBad(self.armHistory[index])
                    if not wasBadTrend:
                        if rewardVal < nrBadRewards:
                            nrBadRewards = rewardVal
                            bestArmIndex = index

        if bestArmIndex == armIndex:
            return random.randint(0, len(arms) - 1)
        return bestArmIndex

    def getAverageReward(self, checkList):
        '''
        Gives the average reward score given the history reward list
        :param checkList: the history reward list
        :return: the average score
        '''
        totalRewardScore = 0
        listLen = len(checkList)
        lastRewardsList = checkList[listLen - CHECK_SIZE: listLen]
        for rew in lastRewardsList:
            totalRewardScore += rew
        return totalRewardScore/CHECK_SIZE

    def lastRewardsGettingBad(self, checkList):
        '''
        Checks whether we have any bad trend in the given history reward list
        Function returns a boolean which determines if the trend was good
        or bad together with the trend counter
        :param checkList: the history reward list
        :return: False/True, badRewardsCounter/50
        '''
        listLen = len(checkList)
        badRewardsCounter = 0
        lastRewardsList = checkList[listLen - CHECK_SIZE: listLen]
        actualRew = lastRewardsList[0]
        averageVal = actualRew
        for i in range(1, len(lastRewardsList)):
            nextReward = lastRewardsList[i]
            averageVal += nextReward
            if actualRew > nextReward:
                badRewardsCounter += 1
            actualRew = nextReward

        if averageVal < 0:
            return True, 50
        return (badRewardsCounter >= CHECK_SIZE * BAD_REWARD_RATE), badRewardsCounter


    def give_feedback(self, arm, reward):
        '''
        Sets the new parameters in the datatypes and checks for trends in
        the given arm's reward history list. The AI also regulates the knowledge
        of the world by changing the expected values
        :param arm: the arm the reward was based on
        :param reward: the given reward given for the used arm
        :return: None
        '''
        arm_index = self.arms.index(arm)
        sum = self.sums[arm_index] + reward
        self.sums[arm_index] = sum
        frequency = self.frequencies[arm_index] + 1
        self.frequencies[arm_index] = frequency
        expected_value = sum / frequency
        self.expected_values[arm_index] = expected_value

        self.armHistory[arm_index].append(reward)

        if len(self.armHistory[arm_index]) >= CHECK_SIZE:
            wasBadTrend, rewardVal = self.lastRewardsGettingBad(self.armHistory[arm_index])
            if wasBadTrend:
                self.expected_values[arm_index] -= EXPECTED_DECREASE_RATE
            else:
                bestArmIndex = 0
                bestAvg = 0
                for i, l in enumerate(self.armHistory):
                    avgScore = self.getAverageReward(l)
                    if avgScore > bestAvg:
                        bestArmIndex = i
                        bestAvg = avgScore
                self.expected_values[bestArmIndex] += EXPECTED_INCREASE_RATE





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
