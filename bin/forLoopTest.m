          %== CODE FOR: ./bin/forLoopTest.m ==%
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 8  % Set stack to top
          addi R12, R0, 1
          sw 0(R14), R12
          subi R14, R14, 4  % Alloc stack for for loop declaration scope
          addi R12, R0, 65
          sw 0(R14), R12
          addi R10, R0, 91
          lw R9, 0(R14)
          clt R11, R9, R10
          sw -4(R14), R11
          lw R11, -4(R14)
f1        bz R11, f2
          nop
          lw R1, 0(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          subi R14, R14, 4  % Alloc stack for for loop declaration scope
          addi R10, R0, 0
          sw 0(R14), R10
          addi R8, R0, 23
          lw R7, 0(R14)
          cle R9, R7, R8
          sw -4(R14), R9
          lw R9, -4(R14)
f3        bz R9, f4
          nop
          subi R14, R14, 4  % Alloc stack for temp scope
          lw R7, 4(R14)
          addi R6, R0, 97
          add R8, R6, R7
          sw 0(R14), R8
          lw R1, 0(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          subi R14, R14, 4  % Alloc stack for for loop declaration scope
          addi R8, R0, 0
          sw 0(R14), R8
          addi R7, R0, 23
          lw R5, 0(R14)
          cle R6, R5, R7
          sw 4(R14), R6
          lw R6, 4(R14)
f5        bz R6, f6
          nop
          subi R14, R14, 4  % Alloc stack for temp scope
          lw R5, 4(R14)
          addi R4, R0, 65
          add R7, R4, R5
          sw 0(R14), R7
          lw R1, 0(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R14, R14, 4  % Dealloc stack for temp scope
          addi R4, R0, 1
          lw R5, 0(R14)
          add R7, R5, R4
          sw 0(R14), R7
          lw R7, 0(R14)
          sw 0(R14), R7
          addi R5, R0, 23
          lw R4, 0(R14)
          cle R7, R4, R5
          sw 4(R14), R7
          lw R6, 4(R14)
          j f5
f6        nop  % End of loop
          addi R14, R14, 4  % Dealloc stack for temp scope
          addi R14, R14, 4  % Dealloc stack for temp scope
          addi R8, R0, 1
          lw R7, 0(R14)
          add R6, R7, R8
          sw -8(R14), R6
          lw R6, -8(R14)
          sw 0(R14), R6
          addi R7, R0, 23
          lw R8, 0(R14)
          cle R6, R8, R7
          sw -4(R14), R6
          lw R9, -4(R14)
          j f3
f4        nop  % End of loop
          addi R14, R14, 4  % Dealloc stack for temp scope
          addi R10, R0, 1
          lw R6, 0(R14)
          add R9, R6, R10
          sw -8(R14), R9
          lw R9, -8(R14)
          sw 0(R14), R9
          addi R6, R0, 91
          lw R10, 0(R14)
          clt R9, R10, R6
          sw -4(R14), R9
          lw R11, -4(R14)
          j f1
f2        nop  % End of loop
          addi R14, R14, 4  % Dealloc stack for temp scope
          addi R12, R0, 64
          lw R9, 0(R14)
          add R11, R9, R12
          sw 4(R14), R11
          lw R1, 4(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines
