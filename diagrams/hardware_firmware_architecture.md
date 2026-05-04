# Firmware Block Diagram

하드웨어, 커널, 펌웨어 계층을 Flowchart, Class Diagram, ER Diagram 세 가지 뷰로 설명합니다.

---

## 1. System Architecture — Flowchart

인터럽트 발생부터 펌웨어 처리까지의 전체 실행 흐름을 나타냅니다.

```mermaid
graph TD
    classDef hw     fill:#ffebee,stroke:#c62828,stroke-width:2px
    classDef kernel fill:#f1f8e9,stroke:#558b2f,stroke-width:2px
    classDef fw     fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef data   fill:#fff3e0,stroke:#e65100,stroke-width:1px,stroke-dasharray:5 5

    subgraph HW [Hardware Layer]
        direction TB
        CPU[RISC-V Vector Core]:::hw
        DMA[DMA Controller]:::hw
        BBA[Baseband Accelerator]:::hw
        MEM[SRAM Memory]:::hw
    end

    subgraph KNL [Kernel and HAL Layer]
        direction TB
        ISR((IRQ Handler)):::kernel
        HAL{HAL API}:::kernel
        Sched[[RTOS Scheduler]]:::kernel
        MQ[Message Queue]:::kernel
    end

    subgraph FWL [Firmware Application Layer]
        direction TB
        MainTask([Main Task]):::fw
        VecMod([Vector Math Module]):::fw
        CommMod([Comm Module]):::fw

        subgraph DS [Data Models]
            Cfg[System Config]:::data
            RxBuf[Rx Ring Buffer]:::data
            TxBuf[Tx Ring Buffer]:::data
        end
    end

    BBA -- 1. HW Interrupt --> ISR
    ISR -- 2. Set Event Flag --> Sched
    Sched -- 3. Unblock Task --> MainTask
    MainTask -- 4. Call HAL --> HAL
    HAL -- 5. Register Write --> DMA
    DMA -. 6 DMA Read .-> RxBuf
    DMA -. 7 DMA Write .-> TxBuf
    MainTask -- 8. Run Algorithm --> VecMod
    VecMod -. 9 Read Params .-> Cfg
    VecMod -. 10 Read Write Data .-> RxBuf
    MainTask -- 11. Enqueue --> MQ
    CommMod -- 12. Dequeue --> MQ
    CommMod -- 13. DMA Tx --> HAL
```

---

## 2. Software Class Structure — Class Diagram

펌웨어 소프트웨어의 주요 클래스와 의존 관계를 나타냅니다.

```mermaid
classDiagram
    class IRQHandler {
        +int irqNum
        +handle(irqNum int) void
        +enable(irqNum int) void
        +disable(irqNum int) void
    }
    class RTOSScheduler {
        +int tickRate
        +schedule() void
        +unblock(taskId int) void
        +setFlag(event int) void
    }
    class HALDriver {
        +init() void
        +dmaRead(addr int, len int) int
        +dmaWrite(addr int, len int) int
        +regWrite(reg int, val int) void
    }
    class MainTask {
        +int priority
        +run() void
        +processData() void
        +sendOutput() void
    }
    class VectorMathModule {
        +compute(data int) float
        +readParams(cfg int) void
    }
    class CommModule {
        +transmit(buf int, len int) int
        +receive(buf int, len int) int
    }
    class RingBuffer {
        +int head
        +int tail
        +int size
        +push(val int) bool
        +pop() int
        +isEmpty() bool
    }
    class SystemConfig {
        +int sampleRate
        +int gain
        +int mode
        +load() void
        +save() void
    }

    IRQHandler --> RTOSScheduler : notifies
    RTOSScheduler --> MainTask : schedules
    MainTask --> HALDriver : uses
    MainTask --> VectorMathModule : delegates
    MainTask --> CommModule : sends via
    VectorMathModule --> SystemConfig : reads
    VectorMathModule --> RingBuffer : readWrite
    HALDriver --> RingBuffer : dma transfer
    CommModule --> RingBuffer : dequeues
```

---

## 3. Data Model — ER Diagram

펌웨어가 관리하는 핵심 데이터 구조와 관계를 나타냅니다.

```mermaid
erDiagram
    SYSTEM_CONFIG {
        int sampleRate
        int gain
        int mode
        int version
    }
    RING_BUFFER {
        int id
        int head
        int tail
        int size
    }
    TASK_CONTEXT {
        int taskId
        int priority
        int stackSize
        int state
    }
    IRQ_TABLE {
        int irqNum
        int priority
        int handlerAddr
        int enabled
    }
    DMA_CHANNEL {
        int channelId
        int srcAddr
        int dstAddr
        int length
    }

    TASK_CONTEXT ||--o{ RING_BUFFER : "reads and writes"
    TASK_CONTEXT }o--|| SYSTEM_CONFIG : "reads"
    DMA_CHANNEL ||--|{ RING_BUFFER : "transfers to"
    IRQ_TABLE ||--o{ TASK_CONTEXT : "triggers"
    DMA_CHANNEL }o--|| TASK_CONTEXT : "owned by"
```
