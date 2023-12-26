from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate


def get_chains(mode="zero-shot", temperature=0.5, streaming=True, model="gpt-4"):
    llm = ChatOpenAI(
        temperature=temperature,
        model=model,
        streaming=streaming,
        callbacks=[
            StreamingStdOutCallbackHandler()
        ]
    )
    
    if mode == "zero-shot":
        explain_template = ChatPromptTemplate.from_messages([
            (
                "system", 
                """
                {explain_role}
                """),
            (
                "human", 
                """
                question:
                {question}

                explanation:
                {explanation}
                """
            )
        ])
        
        split_template = ChatPromptTemplate.from_messages([
            (
                "system", 
                """
                {split_role}
                """
            ),
            (
                "human", 
                """
                quesiton:
                {question}
                
                explanation:
                {explanation}
                """
            )
        ])

        question_template = ChatPromptTemplate.from_messages([
            (
                "system", 
                """
                {question_role}
                """
            ),
            (
                "human", 
                """
                question:
                {question}
                
                explanation steps:
                {steps}
                """
            )
        ])
        
        explain_chain = explain_template | llm
        split_chain = split_template | llm
        question_chain = question_template | llm
        return explain_chain, split_chain, question_chain
    
    elif mode == "few-shot":
        examples = [
            {
                "input": """
                question:
                집합 $X=\{x|x \ge k \}$에 대하여 $X$에서 $X$로의 함수 $f(x)=x^2-6x$가 일대일대응일 때, 상수 $k$의 값을 구하시오.
                
                explanation:
                $y=x^2-6x = (x-3)^2-9$이므로 $y=f(x)$의 그래프는 그림과 같다.  함수 $f$가 일대일대응이 되려면 증가 또는 감소함수의 그래프가 되어야 하므로 $x=3$을 기준으로 어느 한 쪽의 전체 또는 일부분이어야 한다. 따라서 
                $k \ge 3 \qquad \cdots\cdots ㉠$
                또한, 일대일대응이 되려면 함수 $f$의 (치역)=(공역)이어야 하므로 정의역 $\{x|x \ge k\}$에 대하여 치역 $\{y|y \ge k\}$이어야 한다. 따라서 $k=f(k)$에서 
                $$\begin{align*}
                &k=k^2-6k \\
                &k(k-7)=0 \\
                \rightarrow \quad &k=0 \hbox{ 또는 }k=7 \quad \cdots\cdots ㉡
                \end{align*}$$
                ㉠, ㉡에서 구하는 $k$의 값은 $k=7$이다.      
                """,
                "output": """
                [1단계]
                문제에서 구하는 것은 '일대일대응' 상태일 때 k의 값이에요. 일대일대응을 파악하기 위해서는 함수의 그래프를 그려볼까요?

                [2단계]
                $y=x^2-6x = (x-3)^2-9$이므로 $y=f(x)$의 그래프는 그림과 같아요. 이차함수의 그래프를 그릴 땐 꼭지점의 좌표를 알아야하기 때문에 식을 표준형으로 바꿔보아요.

                [3단계]
                '일대일대응'이 되려면 함수 $f$가 증가 또는 감소함수의 그래프가 되어야 해요. 또한 이차함수의 대칭성을 고려한다면, $x=3$을 기준으로 어느 한 쪽의 전체 또는 일부분이어야 한다는 것을 알 수 있어요.

                [4단계]
                $k \ge 3 \qquad \cdots\cdots ㉠$라는 사실을 알 수 있어요. 또한, 일대일대응이 되려면 함수 $f$의 (치역)=(공역)이어야 하는데요, 그렇다면 정의역 $\{x|x \ge k\}$에 대하여 치역 $\{y|y \ge k\}$이어야 해요.

                [5단계]
                $k=f(k)$에서 
                $$\begin{align*}
                &k=k^2-6k \\
                &k(k-7)=0 \\
                \rightarrow \quad &k=0 \hbox{ 또는 }k=7 \quad \cdots\cdots ㉡
                \end{align*}$$
                로 풀었나요?
                마지막으로 앞의 ㉠, ㉡을 연립하여 $k$의 값을 구해보아요.
                """
            },
            {
                "input": """
                question:
                등식 $a(x^2+x+2)+b(x-1)+c=x^2+4x$가 $x$에 대한 항등식일 때, $a^2+b^2+c^2$의 값은? (단, $a$, $b$, $c$는 상수이다.)
                
                explanation:
                주어진 식의 좌변을 전개하여 $x$에 대하여 정리하면 
                $ax^2+(a+b)x+2a-b+c=x^2+4x$
                이고, 양변의 계수를 비교하면 
                $a=1,\quad a+b=4,\quad 2a-b+c=0$
                이다. 세 식을 연립하여 풀면 $a=1$, $b=3$, $c=1$이다. 따라서 구하는 값은 
                $a^2+b^2+c^2=1+9+1=11$
                이다.
                """,
                "output": """
                [1단계]
                $x$에 관한 '항등식'의 '계수'를 묻는 문제입니다. 양변의 계수를 비교하는 '계수비교법'을 사용할 수 있겠네요!

                [2단계]
                주어진 식의 좌변을 전개하여 $x$에 대하여 정리하면 $ax^2+(a+b)x+2a-b+c=x^2+4x$에요.

                [3단계]
                양변의 계수를 비교하면 $a=1,\quad a+b=4,\quad 2a-b+c=0$이 돼요.

                [4단계]
                세 식을 연립하여 풀면 $a=1$, $b=3$, $c=1$이고, $a^2+b^2+c^2=1+9+1=11$의 값을 구할 수 있어요!
                """
            },
            {
                "input": """
                question:
                $x$에 대한 이차방정식 $x^2+(a+2k)x+k^2-2k-b=0$ 이 실수 $k$의 값에 관계없이 항상 중근을 가질 때, 실수 $a$, $b$에 대하여 $a+b$의 값은?
                
                explanation:
                이차방정식 $x^2+(a+2k)x+k^2-2k-b=0$의 판별식을 $D$라 하면
                $$
                \begin{align*}
                &D=(a+2k)^2-4(k^2-2k-b)=0\\
                &a^2+4ak+4k^2-4k^2+8k+4b=0\\
                &(4a+8)k+a^2+4b=0\\
                \end{align*}
                $$
                이고, 이 식이 $k$의 값에 관계없이 항상 성립하므로 $4a+8=0, \quad a^2+4b=0$이다. 따라서 $a=-2$, $b=-1$이므로 구하는 값은 $a+b=-3$이다.
                """,
                "output": """
                [1단계]
                항상 '중근'을 가지는 상황을 해석하는 문제예요. 판별식을 이용해야겠네요!

                [2단계]
                이차방정식 $x^2+(a+2k)x+k^2-2k-b=0$의 판별식을 $D$라고 할게요. 중근을 가질 조건은 $D=0$임을 이용해볼게요.

                [3단계]
                $$\begin{align*}
                &D=(a+2k)^2-4(k^2-2k-b)=0\\
                &a^2+4ak+4k^2-4k^2+8k+4b=0\\
                &(4a+8)k+a^2+4b=0\\
                \end{align*}$$
                이 됩니다.

                [4단계]
                그리고 이 식이 $k$의 값에 관계없이 항상 성립해요. $k$에 관한 항등식이라는 뜻이에요. 항등식의 계수를 구할 수 있는 '미정계수법'을 사용해볼게요.

                [5단계]  
                $4a+8=0, \quad a^2+4b=0$이네요. 따라서 $a=-2$, $b=-1$인데요. 이제 $a+b$의 값을 구할 수 있겠네요!
                """    
            },
            {
                "input": """
                question:
                이차방정식 $x^{2} - kx + k -1 = 0$의 두 근의 비가 $1 : 2$일 때, 모든 실수 $k$의 값의 합은?
                
                explanation:
                이차방정식 $x^{2} - kx + k -1 = 0$의 두 근의 비가 $1:2$이므로 두 근을 $\alpha$, $2 \alpha$라고 하면 근과 계수의 관계에 의하여 
                $\alpha + 2 \alpha = 3\alpha = k \quad\rightarrow\quad \alpha = \dfrac{k}{3} \quad\cdots ㉠$이고
                $\alpha \cdot 2 \alpha = 2 \alpha^{2} = k -1 \quad\cdots ㉡$이다. ㉠을 ㉡에 대입하면 
                $$\begin{align*}
                &2k^{2} -9k +9 - 0\\
                &(2k-3)(k-3) = 0\\
                &\rightarrow\quad k = \dfrac{3}{2} \hbox{ 또는 } k =3
                \end{align*}$$
                이다. 따라서 실수 $k$의 값의 합은 $\dfrac{9}{2}$이다.
                """,
                "output": """
                [1단계]
                두 근이 비례 관계에 있는 상태에서 실수 $k$의 값을 묻는 문제예요. 두 근을 하나의 문자로 표현할 수 있겠네요.

                [2단계]
                이차방정식 $x^{2} - kx + k -1 = 0$의 두 근의 비가 $1:2$이므로 두 근을 $\alpha$, $2 \alpha$라고 표현할 수 있어요.

                [3단계]
                근과 계수의 관계에 의해서 두 근의 합은 일차항의 계수에 마이너스를 곱한 값과 같아요. $\alpha + 2 \alpha = 3\alpha = k \quad\rightarrow\quad \alpha = \dfrac{k}{3} \quad\cdots ㉠$이 돼요.

                [4단계]
                근과 계수의 관계에 의해서 두 근의 곱은 상수항과 같아요. $\alpha \cdot 2 \alpha = 2 \alpha^{2} = k -1 \quad\cdots ㉡$이 돼요.

                [5단계]
                이제 ㉠을 ㉡에 대입하면 
                $$\begin{align*}
                &2k^{2} -9k +9 - 0\\ %-0이 아닌 =0이 되어야 할 것 같습니다.
                &(2k-3)(k-3) = 0\\
                &\rightarrow\quad k = \dfrac{3}{2} \hbox{ 또는 } k =3
                \end{align*}$$
                라는 값을 구할 수 있어요.
                이제 ㉠과 ㉡을 연립하면 원하는 답, 조건을 만족하는 실수 $k$의 값을 얻을 수 있어요.
                """
            },
            {
                "input": """
                question:
                부등식 $x^2+2|x| - 3 \lt 0$을 만족하는 정수 $x$의 개수를 구하시오.
                
                explanation:
                부등식 $ x^2+2|x| - 3 \lt 0 $에서 범위를 나누어보면
                $(\rm i)$ $x \ge 0$일 때, 
                $$\begin{align*}
                & x^2+2x-3 \lt 0\\
                & (x+3)(x-1) \lt 0 \\
                \rightarrow \quad & -3 \lt x \lt 1 
                \end{align*}$$
                이다. 그런데 $x \ge 0$이므로 $0 \le x \lt 1$이다.
                $(\rm ii)$ $x \lt 0$일 때, 
                $$\begin{align*}
                & x^2 - 2x-3 \lt 0 \\
                & (x-3)(x+1) \lt 0 \\
                \rightarrow \quad & -1 \lt x \lt 3 
                \end{align*}$$
                이다. 그런데 $x \lt 0$이므로 $-1 \lt x \lt 0$이다. 
                따라서 $(\rm i)$, $(\rm ii)$에서 $-1 \lt x \lt 1$이므로 부등식을 만족하는 정수 $x$의 개수는 $0$으로 $1$개이다. 
                """,
                "output": """
                [1단계]
                절대값이 포함된 부등식을 해석하는 문제예요. 절대값은 절대값 안이 $0$보다 클 때, $0$보다 작을 때로 나누어 생각해야해요. 부등식 $ x^2+2|x| - 3 \lt 0 $에서 절대값 안의 범위를 나누어서 생각해볼게요.

                [2단계]
                $(\rm i)$ $x \ge 0$일 때, 
                $$\begin{align*}
                & x^2+2x-3 \lt 0\\
                & (x+3)(x-1) \lt 0 \\
                \rightarrow \quad & -3 \lt x \lt 1 
                \end{align*}$$
                이 돼요.

                [3단계]
                그런데 [3단계]의 맨 처음 조건에서 $x \ge 0$이므로 이를 연립하면 $0 \le x \lt 1$이 돼요.

                [4단계]
                $(\rm ii)$ $x \lt 0$일 때, 
                $$\begin{align*}
                & x^2 - 2x-3 \lt 0 \\
                & (x-3)(x+1) \lt 0 \\
                \rightarrow \quad & -1 \lt x \lt 3 
                \end{align*}$$
                이 돼요.

                [5단계]
                $x \lt 0$이므로 이를 연립하면 $-1 \lt x \lt 0$이 돼요. 따라서 $(\rm i)$, $(\rm ii)$에서 $-1 \lt x \lt 1$이 되는데요. 이를 만족하는 정수 $x$는 $0$뿐이죠. 이제 정수 $x$의 개수를 답할 수 있게 됐어요.
                """
            }
    ]

    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "{input}"), ("ai", "{output}"),
    ])

    fs_prompt = FewShotChatMessagePromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
    )

    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_role}"),
        fs_prompt,
        (
            "human", 
            """
            quesiton:
            {question}
            
            explanation:
            {explanation}
            """
         ),
    ])

    return final_prompt | llm