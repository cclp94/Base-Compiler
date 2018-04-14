          %== CODE FOR: ./bin/objectFunctionsTest.m ==%
f1        sw 0(R13), R14
          lw R11, 12(R13)
          lw R10, 8(R13)
          add R12, R10, R11
          sw 16(R13), R12
          lw R12, 16(R13)
          sw 4(R13), R12
          lw R14, 0(R13)
          jr R14
f2        sw 0(R13), R14
          lw R10, 12(R13)
          lw R11, 8(R13)
          sub R12, R11, R10
          sw 16(R13), R12
          lw R12, 16(R13)
          sw 4(R13), R12
          lw R14, 0(R13)
          jr R14
f3        sw 0(R13), R14
          lw R11, 12(R13)
          lw R10, 8(R13)
          mul R12, R10, R11
          sw 16(R13), R12
          lw R12, 16(R13)
          sw 4(R13), R12
          lw R14, 0(R13)
          jr R14
f4        sw 0(R13), R14
          lw R10, 12(R13)
          lw R11, 8(R13)
          div R12, R11, R10
          sw 16(R13), R12
          lw R12, 16(R13)
          sw 4(R13), R12
          lw R14, 0(R13)
          jr R14
f5        sw 0(R13), R14
          addi R11, R0, 1
          lw R10, 8(R13)
          cle R12, R10, R11
          sw -4(R13), R12
          lw R12, -4(R13)
          bz R12, f7  % If Statement
f6        nop
          addi R11, R0, 1
          sw 4(R13), R11
          j f8
f7        nop
          subi R13, R13, 12  % Alloc stack for temp scope
          addi R10, R0, 1
          lw R9, 20(R13)
          sub R11, R9, R10
          sw 8(R13), R11
          lw R11, 8(R13)
          sw -4(R13), R11  % Copy parameter
          addi R13, R13, -12
          jl R14, f5
          addi R13, R13, 12
          lw R9, -8(R13)
          sw 4(R13), R9
          lw R9, 4(R13)
          lw R10, 20(R13)
          mul R11, R10, R9
          sw 0(R13), R11
          lw R11, 0(R13)
          sw 16(R13), R11
          addi R13, R13, 12  % Dealloc stack for temp scope
f8        nop  % If statement end
          lw R14, 0(R13)
          jr R14
f9        sw 0(R13), R14
          lw R11, 12(R13)
          lw R10, 8(R13)
          add R12, R10, R11
          sw 16(R13), R12
          lw R12, 16(R13)
          sw 4(R13), R12
          lw R14, 0(R13)
          jr R14
          entry  % program entry
          align
          addi R13, R0, topaddr  % init stack pointer register
          addi R14, R0, topaddr  % init frame pointer register
          subi R13, R13, 36  % Set stack to top
          addi R12, R0, 60
          sw -12(R13), R12  % Copy parameter
          addi R10, R0, 5
          sw -8(R13), R10  % Copy parameter
          addi R13, R13, -20
          jl R14, f9
          addi R13, R13, 20
          lw R11, -16(R13)
          sw 8(R13), R11
          lw R10, 8(R13)
          putc R10
          addi R10, R0, 60
          sw -12(R13), R10  % Copy parameter
          addi R12, R0, 5
          sw -8(R13), R12  % Copy parameter
          addi R13, R13, -20
          jl R14, f1
          addi R13, R13, 20
          lw R11, -16(R13)
          sw 12(R13), R11
          lw R12, 12(R13)
          putc R12
          addi R12, R0, 70
          sw -12(R13), R12  % Copy parameter
          addi R10, R0, 5
          sw -8(R13), R10  % Copy parameter
          addi R13, R13, -20
          jl R14, f2
          addi R13, R13, 20
          lw R11, -16(R13)
          sw 16(R13), R11
          lw R10, 16(R13)
          putc R10
          addi R10, R0, 35
          sw -12(R13), R10  % Copy parameter
          addi R12, R0, 2
          sw -8(R13), R12  % Copy parameter
          addi R13, R13, -20
          jl R14, f3
          addi R13, R13, 20
          lw R11, -16(R13)
          sw 20(R13), R11
          lw R12, 20(R13)
          sw 0(R13), R12
          lw R12, 0(R13)
          putc R12
          addi R12, R0, 120
          sw -12(R13), R12  % Copy parameter
          addi R10, R0, 2
          sw -8(R13), R10  % Copy parameter
          addi R13, R13, -20
          jl R14, f4
          addi R13, R13, 20
          lw R11, -16(R13)
          sw 24(R13), R11
          lw R12, 24(R13)
          addi R11, R0, 5
          add R10, R11, R12
          sw 28(R13), R10
          lw R10, 28(R13)
          sw 4(R13), R10
          lw R10, 4(R13)
          putc R10
          addi R10, R0, 4
          sw -4(R13), R10  % Copy parameter
          addi R13, R13, -12
          jl R14, f5
          addi R13, R13, 12
          lw R11, -8(R13)
          sw 32(R13), R11
          lw R10, 32(R13)
          putc R10
          hlt  % program exit
          %== END OF PROGRAM ==%
