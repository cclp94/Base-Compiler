          %== CODE FOR: ./bin/fibonacciTest.m ==%
f1        sw 0(R14), R15
          addi R11, R0, 2
          lw R10, 8(R14)
          cle R12, R10, R11
          sw -8(R14), R12
          lw R12, -8(R14)
          bz R12, f3  % If Statement
f2        nop
          addi R11, R0, 1
          sw 4(R14), R11
          j f4
f3        nop
          addi R10, R0, 3
          lw R9, 8(R14)
          ceq R11, R9, R10
          sw -8(R14), R11
          lw R11, -8(R14)
          bz R11, f6  % If Statement
f5        nop
          addi R10, R0, 2
          sw 4(R14), R10
          j f7
f6        nop
          subi R14, R14, 20  % Alloc stack for temp scope
          addi R9, R0, 2
          lw R8, 28(R14)
          sub R10, R8, R9
          sw 8(R14), R10
          lw R10, 8(R14)
          sw -4(R14), R10  % Copy parameter
          addi R14, R14, -12
          jl R15, f1
          addi R14, R14, 12
          lw R8, -8(R14)
          sw 4(R14), R8
          addi R8, R0, 1
          lw R9, 28(R14)
          sub R10, R9, R8
          sw 16(R14), R10
          lw R10, 16(R14)
          sw -4(R14), R10  % Copy parameter
          addi R14, R14, -12
          jl R15, f1
          addi R14, R14, 12
          lw R9, -8(R14)
          sw 12(R14), R9
          lw R9, 4(R14)
          lw R8, 12(R14)
          add R10, R8, R9
          sw 0(R14), R10
          lw R10, 0(R14)
          sw 24(R14), R10
          addi R14, R14, 20  % Dealloc stack for temp scope
f7        nop  % If statement end
f4        nop  % If statement end
          lw R15, 0(R14)
          jr R15
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 4  % Set stack to top
          addi R12, R0, 30
          sw -4(R14), R12  % Copy parameter
          addi R14, R14, -12
          jl R15, f1
          addi R14, R14, 12
          lw R11, -8(R14)
          sw 0(R14), R11
          lw R1, 0(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines
