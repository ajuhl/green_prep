import math
import numpy as np
from numpy import linalg as la

def vertcat(arr1,arr2):
    return np.concatenate((arr1,arr2),axis=0)
def horzcat(arr1,arr2):
    return np.concatenate((arr1,arr2),axis=1)

def findPivotRow(T,pivotColumn,lastColumn,m):
    min = float('inf')
    for i in range(m):
        if T[i,pivotColumn] > 0:
            quotient = T[i,lastColumn]/T[i,pivotColumn]
            #print "quotient"
            #print(quotient)
            if quotient<min:
                min = quotient
                pivotRow = i
    return pivotRow

def gaussianElimination(T,pRow,pCol,m):
    T[pRow] = T[pRow]/T[pRow,pCol]
    for i in range(m):
        if i!=pRow:
            T[i] = T[i] - T[pRow]*T[i,pCol]
    return T

def findPivotColumn(T,m,n):
    pivotColumn = -1
    min = -1e-5
    for i in range(m):
        for j in range(n):
            #print(i,j,T[i,j])
            if T[i,j] < min:
                min = T[i,j]
                pivotColumn = j
    #print "min"
    #print(min)
    return pivotColumn

def simplexSolution(T,mC,nC,mT,nT):
    x = np.zeros((nC,1),dtype=float)
    for j in range(nC):
        cont = True
        found = -1
        for i in range(mT):
            if T[i,j]==1.0 and found==-1:
                found = i
            elif T[i,j]==0.0:
                cont = True
            else:
                cont = False
                break
        if cont and found!=-1 and i==mT-1:
            x[j,0] = T[found,nT-1]
    return x

def simplexMacro(Foods,Constraints,upperBounds):
    goalMacros = upperBounds[0:3]
    (mF,nF) = np.shape(Foods)
    (mC,nC) = np.shape(Constraints)

    tableau = horzcat(horzcat(vertcat(Constraints, -Foods),np.eye(mF+mC)),vertcat(upperBounds,np.zeros((mF,1),dtype=float)))
    (mT,nT) = np.shape(tableau)

    print "tableau"
    print(tableau)

    pivotColumn = findPivotColumn(tableau[mC:mT,0:nT-1],mF,nT-1)
    pivotCount = 1
    while pivotColumn!=-1 and pivotCount<=nC:
        pivotRow = findPivotRow(tableau,pivotColumn,nT-1,mC)
        tableau = gaussianElimination(tableau,pivotRow,pivotColumn,mT)
        pivotCount = pivotCount+1
        #print (tableau)
        pivotColumn = findPivotColumn(tableau[mC:mT,0:nT-1],mF,nT-1)

    servingSizes = simplexSolution(tableau,mC,nC,mT,nT)
    mealMacros = tableau[mT-mF:mT-1,nT-1]
    carryOver = goalMacros - mealMacros
    #if goalMacros != np.array([[0],[0],[0]]):
        #mealQuality = la.norm(mealMacros - goalMacros)/la.norm(goalMacros)
    #else:
        #mealQuality = 0

    return servingSizes

def getFoodComposition(food):
    if food == 'chicken':
        composition = np.array([[18.75,0,3.57]])
    elif food == 'steak':
        composition = np.array([[29.33,0,9.67]])
    elif food == 'red potato':
        composition = np.array([[2.03,17.57,0]])
    elif food == 'quinoa':
        composition = np.array([[4.4,21.3,1.92]])
    elif food == 'butter':
        composition = np.array([[0,0,78.75]])
    elif food == 'hummus':
        composition = np.array([[6.67,13.33,6.67]])
    elif food == 'pizza':
        composition = np.array([[8.63,30.22,10.79]])
    elif food == 'ice cream':
        composition = np.array([[5,30,5]])
    else:
        composition = np.array([[1,1,1]])
    return composition

def main():
    goalMacros = np.zeros((3,1),dtype=float)
    goalMacros[0,0] = input("Protein Goal: ")
    goalMacros[1,0] = input("Carb Goal: ")
    goalMacros[2,0] = input("Fat Goal: ")

    numberOfFoods = input("How many foods would you like to choose? (max 8): ")
    foodComposition = np.zeros((3,numberOfFoods),dtype=float)
    foods = []
    upperBounds = np.zeros((numberOfFoods,1),dtype=float)
    for i in range(numberOfFoods):
        food = raw_input("\nSelect a food:\nchicken\nsteak\nred potato\nquinoa\nbutter\nhummus\npizza\nice cream\n-->")
        foodComposition[:,i] = getFoodComposition(food)
        foods.append(food)
        upperBounds[i,0] = float('inf')

    lConstraints = vertcat(foodComposition,np.eye(numberOfFoods))
    rConstraints = vertcat(goalMacros,upperBounds)
    servingSizes=simplexMacro(foodComposition,lConstraints,rConstraints)
    for i in range(numberOfFoods):
        print foods[i]+": "
        print str(int(round(servingSizes[i,0]*100)))+'g'

if __name__ == '__main__':
    main()
