# Hardware-Firmware Architecture

아래는 하드웨어, 커널, 펌웨어 계층의 상호작용을 나타내는 Mermaid 다이어그램입니다. 원본에서 누락된 대괄호를 보정했습니다.

```mermaid
graph TD
    %% 1. 스타일 정의 (구분을 명확히 하기 위해 색상 및 테두리 설정)
    classDef hardware fill:#ffebee,stroke:#c62828,stroke-width:2px;
    classDef kernel fill:#f1f8e9,stroke:#558b2f,stroke-width:2px;
    classDef firmware fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef dataClass fill:#fff3e0,stroke:#e65100,stroke-width:1px,stroke-dasharray: 5 5;

    %% 2. 하드웨어 영역
    subgraph HW_Layer [Hardware Layer]
        direction TB
        Core[RISC-V Vector Core]:::hardware
        DMA[DMA Controller]:::hardware
        BBA[Baseband Accelerator]:::hardware
    end

    %% 3. 커널 / OS 영역
    subgraph Kernel_Layer [Kernel / HAL Layer]
        direction TB
        ISR((HW Interrupt Handler)):::kernel
        HAL{HAL API}:::kernel
        Sched[[RTOS Scheduler]]:::kernel
    end

    %% 4. 펌웨어 어플리케이션 및 클래스(구조체) 영역
    subgraph FW_App_Layer [Firmware Application Layer]
        direction TB
        
        Task_Main([Main Processing Task]):::firmware
        Module_VecCalc([Vector Math Module]):::firmware
        
        %% 클래스/구조체 성격을 나타내는 서브그래프
        subgraph Data_Structures [Data Models / Context]
            Context_Config[System Config Class]:::dataClass
            Buffer_RxRx[Tx/Rx Ring Buffer]:::dataClass
        end
    end

    %% 5. 상호작용 및 실행 흐름 (플로우차트 성격)
    
    %% 하드웨어 -> 커널 흐름 (인터럽트)
    BBA -- 1. H/W Interrupt --> ISR
    
    %% 커널 -> 펌웨어 흐름 (스케줄링)
    ISR -- 2. Set Event/Flag --> Sched
    Sched -- 3. Context Switch & Unblock --> Task_Main
    
    %% 펌웨어 -> 하드웨어 제어 (HAL 경유)
    Task_Main -- 4. Call API for DMA Tx/Rx --> HAL
    HAL -- 5. Register Write --> DMA
    DMA -. 6. Memory Direct Access .-> Buffer_RxRx
    
    %% 펌웨어 내부 로직 처리 (메서드 호출 및 데이터 접근)
    Task_Main -- 7. Run Algorithm --> Module_VecCalc
    Module_VecCalc -. 8. Read Parameters .-> Context_Config
    Module_VecCalc -. 9. Read/Write Data .-> Buffer_RxRx
```

