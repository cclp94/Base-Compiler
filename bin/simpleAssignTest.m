          %== CODE FOR: ./bin/simpleAssignTest.m ==%
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 12  % Set stack to top
          addi R12, R0, 65
          sw 0(R14), R12
          addi R12, R0, 70
          sw 4(R14), R12
          addi R12, R0, 97
          sw 8(R14), R12
          lw R1, 0(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          lw R1, 8(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          lw R1, 4(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          lw R12, 0(R14)
          sw 4(R14), R12
          lw R1, 4(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines
