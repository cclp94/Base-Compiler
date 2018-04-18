          %== CODE FOR: ./bin/objectAttributeTest.m ==%
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 16  % Set stack to top
          addi R12, R0, 8
          sw 4(R14), R12
          addi R12, R0, 4
          sw 8(R14), R12
          addi R11, R0, 61
          lw R10, 8(R14)
          add R12, R10, R11
          sw 12(R14), R12
          lw R1, 12(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines
