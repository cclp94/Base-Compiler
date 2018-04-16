          %== CODE FOR: ./bin/objectFunctionsTest.m ==%
f1        sw 0(R14), R15
          lw R11, 12(R14)
          lw R10, 8(R14)
          add R12, R10, R11
          sw 16(R14), R12
          lw R12, 16(R14)
          sw 4(R14), R12
          lw R15, 0(R14)
          jr R15
f2        sw 0(R14), R15
          lw R10, 12(R14)
          lw R11, 8(R14)
          sub R12, R11, R10
          sw 16(R14), R12
          lw R12, 16(R14)
          sw 4(R14), R12
          lw R15, 0(R14)
          jr R15
f3        sw 0(R14), R15
          lw R11, 12(R14)
          lw R10, 8(R14)
          mul R12, R10, R11
          sw 16(R14), R12
          lw R12, 16(R14)
          sw 4(R14), R12
          lw R15, 0(R14)
          jr R15
f4        sw 0(R14), R15
          lw R10, 12(R14)
          lw R11, 8(R14)
          div R12, R11, R10
          sw 16(R14), R12
          lw R12, 16(R14)
          sw 4(R14), R12
          lw R15, 0(R14)
          jr R15
f5        sw 0(R14), R15
          addi R11, R0, 1
          lw R10, 8(R14)
          cle R12, R10, R11
          sw -8(R14), R12
          lw R12, -8(R14)
          bz R12, f7  % If Statement
f6        nop
          addi R11, R0, 1
          sw 4(R14), R11
          j f8
f7        nop
          subi R14, R14, 12  % Alloc stack for temp scope
          addi R10, R0, 1
          lw R9, 20(R14)
          sub R11, R9, R10
          sw 8(R14), R11
          lw R11, 8(R14)
          sw -4(R14), R11  % Copy parameter
          addi R14, R14, -12
          jl R15, f5
          addi R14, R14, 12
          lw R9, -8(R14)
          sw 4(R14), R9
          lw R9, 4(R14)
          lw R10, 20(R14)
          mul R11, R10, R9
          sw 0(R14), R11
          lw R11, 0(R14)
          sw 16(R14), R11
          addi R14, R14, 12  % Dealloc stack for temp scope
f8        nop  % If statement end
          lw R15, 0(R14)
          jr R15
f9        sw 0(R14), R15
          lw R11, 12(R14)
          lw R10, 8(R14)
          add R12, R10, R11
          sw 16(R14), R12
          lw R12, 16(R14)
          sw 4(R14), R12
          lw R15, 0(R14)
          jr R15
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 40  % Set stack to top
          addi R12, R0, 60
          sw -12(R14), R12  % Copy parameter
          addi R10, R0, 5
          sw -8(R14), R10  % Copy parameter
          addi R14, R14, -20
          jl R15, f9
          addi R14, R14, 20
          lw R11, -16(R14)
          sw 8(R14), R11
          lw R1, 8(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R10, R0, 60
          sw -12(R14), R10  % Copy parameter
          addi R12, R0, 5
          sw -8(R14), R12  % Copy parameter
          addi R14, R14, -20
          jl R15, f1
          addi R14, R14, 20
          lw R11, -16(R14)
          sw 12(R14), R11
          lw R1, 12(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R12, R0, 70
          sw -12(R14), R12  % Copy parameter
          addi R10, R0, 5
          sw -8(R14), R10  % Copy parameter
          addi R14, R14, -20
          jl R15, f2
          addi R14, R14, 20
          lw R11, -16(R14)
          sw 16(R14), R11
          lw R1, 16(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R10, R0, 35
          sw -12(R14), R10  % Copy parameter
          addi R12, R0, 2
          sw -8(R14), R12  % Copy parameter
          addi R14, R14, -20
          jl R15, f3
          addi R14, R14, 20
          lw R11, -16(R14)
          sw 20(R14), R11
          lw R12, 20(R14)
          sw 0(R14), R12
          lw R1, 0(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R12, R0, 120
          sw -12(R14), R12  % Copy parameter
          addi R10, R0, 2
          sw -8(R14), R10  % Copy parameter
          addi R14, R14, -20
          jl R15, f4
          addi R14, R14, 20
          lw R11, -16(R14)
          sw 24(R14), R11
          lw R12, 24(R14)
          addi R11, R0, 5
          add R10, R11, R12
          sw 28(R14), R10
          lw R10, 28(R14)
          sw 4(R14), R10
          lw R1, 4(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R10, R0, 4
          sw -4(R14), R10  % Copy parameter
          addi R14, R14, -12
          jl R15, f5
          addi R14, R14, 12
          lw R11, -8(R14)
          sw 32(R14), R11
          addi R11, R0, 41
          lw R12, 32(R14)
          add R10, R12, R11
          sw 36(R14), R10
          lw R1, 36(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines
