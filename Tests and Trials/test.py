import random
from fractions import Fraction

list_of_bedmas_equations = ['__?__','(__?__)?__','__?__?__','__**(__?__)','__**__?__','__?(__?__)']
list_of_algebra_equations = []

operator_functions = {
    '+': lambda a, b: a + b, 
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b, 
}
operators = ["+","-","*",'/']
currentDifficulty = "Normal"
def bedmas():
    string = random.choice(list_of_bedmas_equations)
    wronganswers = []
    easy_multipliers = [(1,10),(1,2),(1,5)]
    normal_multipliers = [(1,50),(1,3),(1,10)]
    hard_multipliers = [(1,99),(1,3),(1,12)]

    if currentDifficulty == "Easy":
        difficulty_multiplier = easy_multipliers
    elif currentDifficulty == "Normal":
        difficulty_multiplier = normal_multipliers
    else:
        difficulty_multiplier = hard_multipliers



    for i in range(string.count('?')):
        if string.count('**'):
            operator = operators[random.randint(0,1)]
        else:
            operator = random.choice(operators)
        
        string = string.replace('?',operator,1)


    if string == ('__/__'):
        answer = random.randint(difficulty_multiplier[2][0],difficulty_multiplier[2][1])
        random_num = random.randint(difficulty_multiplier[2][0],difficulty_multiplier[2][1])
        string = string.replace('__',str(answer*random_num),1)
        string = string.replace('__',str(random_num),1)

    elif string.count('**')>0:
        for i in range(string.count('__')):
            randomrange = random.randint(difficulty_multiplier[1][0],difficulty_multiplier[1][1])
            string = string.replace('__',str(randomrange),1)

    else:
        for i in range(string.count('__')):
            if string.count('*')>0 or string.count('/'):
                randomrange = random.randint(difficulty_multiplier[2][0],difficulty_multiplier[2][1])
            else:
                randomrange = random.randint(difficulty_multiplier[0][0],difficulty_multiplier[0][1])
            string = string.replace('__',str(randomrange),1)

    answer = eval(string)
    if isinstance (answer,float):
        answer = Fraction(answer).limit_denominator()
    if abs(answer) < 10:
        randomlist = random.sample(range(1,5), 3)
    else:
        randomlist = random.sample(range(1,50),3)
    
    for i in range(0,3):
        if string.count('*')>0:
            operator = operators[random.randint(0,2)]
        else:
            operator = operators[random.randint(0,1)]
        wronganswers.append(operator_functions[operator](answer, randomlist[i]))
        if isinstance (wronganswers[i],float):
            wronganswers[i] = Fraction(wronganswers[i])

    print(str(string)+'='+str(answer),str(wronganswers[0]),str(wronganswers[1]),str(wronganswers[2]))

def fraction():
    easy_multipliers = (1,10)
    normal_multipliers = (1,20)
    hard_multipliers = (1,20)

    if currentDifficulty == "Easy":
        difficulty_multiplier = easy_multipliers
        df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        df2 = df1
        while float(nf1/df1).is_integer():
            df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            df2 = df1
            nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
    elif currentDifficulty == "Normal":
        difficulty_multiplier = normal_multipliers
        df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        df2 = df1
        while float(nf1/df1).is_integer():
            df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            df2 = df1
            nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
    else:
        difficulty_multiplier = hard_multipliers
        nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        df2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        while float(nf1/df1).is_integer():
            df1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            nf1 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
        while float(nf2/df2).is_integer():
            nf2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])
            df2 = random.randint(difficulty_multiplier[0],difficulty_multiplier[1])

    wronganswers = []


    fraction1 = Fraction(nf1,df1) 
    fraction2 = Fraction(nf2,df2)
    
    operator = random.choice(operators)
    string = '('+str(fraction1)+') '+str(operator)+' ('+str(fraction2)+')'
    answer = Fraction(eval(string)).limit_denominator()
    for i in range(3):
        wrong_fraction = Fraction(random.randint(1,20),random.randint(1,20))
        operator = operators[random.randint(0,1)]
        wronganswers.append(operator_functions[operator](answer, wrong_fraction))
    print(str(string)+'='+str(answer),wronganswers[0],wronganswers[1],wronganswers[2])

def algebra():
    question = ('__*x=__')
    runs = 0
    wronganswers = []
    easy_multipliers = [(1,5),0.8]
    normal_multipliers = [(1,10),0.7]
    hard_multipliers = [(1,15),0.55]

    if currentDifficulty == "Easy":
        difficulty_multiplier = easy_multipliers
    elif currentDifficulty == "Normal":
        difficulty_multiplier = normal_multipliers
    else:
        difficulty_multiplier = hard_multipliers

    while question.count('__') > 0:
        if random.random() > difficulty_multiplier[1]+(0.1*runs):
            question = question.replace('__','__*x',1)
        if random.random() > difficulty_multiplier[1]+(0.25*runs):
            question = question.replace('__','(__?__)',1)
        elif random.random()>difficulty_multiplier[1]+(0.2*runs):
            question = question.replace('__*x','(__*x?__)',1)
        if question.count('x')>1:
            if question.count(')*x')>0:
                if random.random()>0.3+(0.1*runs):
                    question = question.replace(")*x",')',1)
    
        multiplier = 1
        if random.random()>0.6:
            multiplier = -multiplier

        question = question.replace('__',str(multiplier*(random.randint(difficulty_multiplier[0][0],difficulty_multiplier[0][1]))),1)
        runs += 1
    for i in range(question.count('?')):
        operator = random.choice(operators)
        question = question.replace('?',operator,1)
    try:
        answer = solve(question)
    except:
        algebra()
    else:
        answer = solve(question)
        if isinstance(answer,float):
            answer = Fraction(answer).limit_denominator()
        
        randomlist = random.sample(range(1,5), 3)
        for i in range(3):
            operator = operators[random.randint(0,1)]
            wronganswers.append(operator_functions[operator](answer, randomlist[i]))
            if isinstance (wronganswers[i],float):
                wronganswers[i] = Fraction(wronganswers[i])

        print(str(question)+'='+str(answer),wronganswers[0],wronganswers[1],wronganswers[2])

def solve(equation,var='x'):
    expression = equation.replace("=","-(")+")"
    grouped = eval(expression.replace(var,'1j'))
    return -grouped.real/grouped.imag

