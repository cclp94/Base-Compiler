          %== CODE FOR: ./bin/functionCallTest.m ==%
f1        sw 0(R14), R15
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
          subi R14, R14, 20  % Set stack to top
          addi R12, R0, 60
          sw 0(R14), R12
          addi R12, R0, 5
          sw 4(R14), R12
          lw R12, 0(R14)
          sw -12(R14), R12  % Copy parameter
          lw R10, 4(R14)
          sw -8(R14), R10  % Copy parameter
          addi R14, R14, -20
          jl R15, f1
          addi R14, R14, 20
          lw R11, -16(R14)
          sw 12(R14), R11
          lw R10, 12(R14)
          sw 8(R14), R10
          lw R10, 8(R14)
          sw -12(R14), R10  % Copy parameter
          lw R12, 4(R14)
          sw -8(R14), R12  % Copy parameter
          addi R14, R14, -20
          jl R15, f1
          addi R14, R14, 20
          lw R11, -16(R14)
          sw 16(R14), R11
          lw R1, 16(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          lw R1, 8(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines
