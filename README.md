# Mermaid Examples

여러 종류의 Mermaid 차트 예제를 모아둔 저장소입니다. GitHub에서 README를 열어 다이어그램 렌더링을 확인하세요.

---

## Flowchart
```mermaid
flowchart TD
  A[Start] --> B{Is it working?}
  B -- Yes --> C[Celebrate]
  B -- No --> D[Fix it]
  D --> B
```

## Sequence Diagram
```mermaid
sequenceDiagram
  participant Alice
  participant Bob
  Alice->>Bob: Hello Bob, how are you?
  Bob-->>Alice: I am good thanks!
```

## Gantt Chart
```mermaid
gantt
  title Project Timeline
  dateFormat  YYYY-MM-DD
  section Development
  Planning      :a1, 2026-05-01, 7d
  Implementation:after a1, 14d
  Testing       : 2026-05-22, 5d
```

## Class Diagram
```mermaid
classDiagram
  class Animal {
    +String name
    +int age
    +void makeSound()
  }
  class Dog {
    +String breed
    +void bark()
  }
  Animal <|-- Dog
```

## State Diagram
```mermaid
stateDiagram-v2
  [*] --> Idle
  Idle --> Running : start
  Running --> Paused : pause
  Paused --> Running : resume
  Running --> Idle : stop
```

## Entity Relationship (ER) Diagram
```mermaid
erDiagram
  CUSTOMER ||--o{ ORDER : places
  ORDER ||--|{ LINE_ITEM : contains
  CUSTOMER }|..|{ DELIVERY_ADDRESS : uses
```

## Pie Chart
```mermaid
pie
  title Market Share 2026
  "Product A" : 45
  "Product B" : 25
  "Product C" : 30
```

## Git Graph
```mermaid
gitGraph
  commit id: "Initial commit"
  branch develop
  commit id: "Add feature"
  checkout main
  merge develop
```

## Journey
```mermaid
journey
  title User Signup
  section Sign up
    Visit site: 5: User
    Fill form: 3: User
    Confirm email: 2: User
```

---

뷰어: GitHub, VSCode의 Mermaid 플러그인, 또는 https://mermaid.live/ 에 붙여넣어 확인하세요.

