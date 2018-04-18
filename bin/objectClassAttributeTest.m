          %== CODE FOR: ./bin/objectClassAttributeTest.m ==%
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 8  % Set stack to top
          addi R12, R0, 65
          sw 4(R14), R12
          lw R1, 4(R14)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines
