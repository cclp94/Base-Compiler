          %== CODE FOR: ./bin/ifStatTest.m ==%
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 12  % Set stack to top
          addi R12, R0, 10
          sw 4(R14), R12
          addi R12, R0, 60
          sw 0(R14), R12
          addi R11, R0, 60
          lw R10, 0(R14)
          cne R12, R10, R11
          sw -8(R14), R12
          lw R12, -8(R14)
          bz R12, f2  % If Statement
f1        nop
          subi R14, R14, 8  % Alloc stack for temp scope
          addi R11, R0, 5
          sw 4(R14), R11
          lw R10, 4(R14)
          lw R9, 8(R14)
          add R11, R9, R10
          sw 0(R14), R11
          lw R1, 0(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R14, R14, 8  % Dealloc stack for temp scope
          j f3
f2        nop
          subi R14, R14, 8  % Alloc stack for temp scope
          addi R11, R0, 20
          sw 4(R14), R11
          lw R9, 4(R14)
          lw R10, 8(R14)
          add R11, R10, R9
          sw 0(R14), R11
          lw R1, 0(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R14, R14, 8  % Dealloc stack for temp scope
f3        nop  % If statement end
          addi R11, R0, 60
          lw R10, 0(R14)
          cge R12, R10, R11
          sw -8(R14), R12
          lw R12, -8(R14)
          bz R12, f5  % If Statement
f4        nop
          subi R14, R14, 8  % Alloc stack for temp scope
          addi R11, R0, 5
          sw 4(R14), R11
          lw R10, 4(R14)
          lw R9, 8(R14)
          add R11, R9, R10
          sw 0(R14), R11
          lw R1, 0(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R14, R14, 8  % Dealloc stack for temp scope
          j f6
f5        nop
          subi R14, R14, 8  % Alloc stack for temp scope
          addi R11, R0, 20
          sw 4(R14), R11
          lw R9, 4(R14)
          lw R10, 8(R14)
          add R11, R10, R9
          sw 0(R14), R11
          lw R1, 0(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R14, R14, 8  % Dealloc stack for temp scope
f6        nop  % If statement end
          lw R11, 4(R14)
          lw R10, 0(R14)
          add R12, R10, R11
          sw 8(R14), R12
          lw R1, 8(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines
