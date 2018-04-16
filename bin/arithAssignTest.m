          %== CODE FOR: ./bin/arithAssignTest.m ==%
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 28  % Set stack to top
          addi R12, R0, 60
          sw 0(R14), R12
          addi R12, R0, 5
          sw 4(R14), R12
          lw R11, 4(R14)
          lw R10, 4(R14)
          mul R12, R10, R11
          sw 12(R14), R12
          lw R10, 12(R14)
          lw R11, 0(R14)
          add R12, R11, R10
          sw 16(R14), R12
          lw R12, 16(R14)
          sw 8(R14), R12
          lw R11, 4(R14)
          lw R10, 0(R14)
          add R12, R10, R11
          sw 20(R14), R12
          lw R1, 20(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R10, R0, 24
          lw R11, 4(R14)
          mul R12, R11, R10
          sw 24(R14), R12
          lw R12, 24(R14)
          sw 4(R14), R12
          lw R1, 8(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          lw R1, 4(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines
