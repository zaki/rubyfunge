require File.join(File.dirname(__FILE__), '..', 'rubyfunge')
require "spec"

describe "RubyFunge" do
  before(:each) do
    @rbf = RubyFunge.new
  end

  it "should go right" do
    @rbf.run('>>>>>>>>>>@')
    @rbf.x.should == 10
    @rbf.y.should == 0
  end

  it "should go down" do
    @rbf.run(
<<-EOS
v
@
EOS
)
    @rbf.x.should == 0
    @rbf.y.should == 1
  end

  it "should push numbers on the stack" do
    @rbf.run('0123456789@')
    @rbf.x.should == 10
    @rbf.y.should == 0
    @rbf.stack.should == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  end

  it "should pop numbers from the stack" do
    @rbf.run('0123456789$$$$$@')
    @rbf.x.should == 15
    @rbf.y.should == 0
    @rbf.stack.should == [0, 1, 2, 3, 4]
  end

  it "should add numbers on the stack" do
    @rbf.run('35+@')
    @rbf.stack.should == [8]
  end

  it "should subtract numbers on the stack" do
    @rbf.run('53-@')
    @rbf.stack.should == [2]
  end

  it "should return 0 when stack is empty" do
    @rbf.run('+@')
    @rbf.stack.should == [0]
  end

  it "should multiply numbers on the stack" do
    @rbf.run('35*@')
    @rbf.stack.should == [15]
  end

  it "should divide numbers on the stack" do
     @rbf.run('62/@')
     @rbf.stack.should == [3]
  end

  it "should modulo divide numbers on the stack" do
     @rbf.run('72%@')
     @rbf.stack.should == [1]
  end

  it "should push result of not" do
     @rbf.run('0!5!@')
     @rbf.stack.should == [1, 0]
  end

  it "should push result of greater than" do
     @rbf.run('91`19`@')
     @rbf.stack.should == [0, 1]
  end

  it "should go in a random direction" do
    @rbf.run(<<EOS
>v
^?012@
^<
EOS
)
    @rbf.stack.should == [0, 1, 2]
  end

  it "should honor left-right selector" do
    @rbf.run(<<EOS
0_>>>>>v
@_1<<<<<
EOS
)
  @rbf.stack.length.should == 0
  end

  it "should honor up-down selector" do
    @rbf.run(<<EOS
0|1@  >@
 >>>>1|
      >3@
EOS
)
  @rbf.stack.length.should == 0
  end

  it "should start ascii mode" do
    @rbf.run('"!dlrow ,olleH"123@')
    @rbf.stack.should == 'Hello, world!'.reverse.split(//).map {|c| c[0]} + [1, 2, 3]
  end

  it "should duplicate values on the stack" do
    @rbf.run('5:@')
    @rbf.stack.should == [5, 5]
  end

  it "should swap values on the stack" do
    @rbf.run('51\@')
    @rbf.stack.should == [1, 5]
  end

  it "should print integer from stack" do
    result = redirect_stdout do
      @rbf.run('15.@')
    end
    result.should == '5'
  end

  it "should print string from stack" do
    result = redirect_stdout do
      @rbf.run('91+6*5+,@')
    end
    result.should == 'A'
  end

  it "should skip next instruction" do
    @rbf.run('1#23#45#6@')
    @rbf.stack.should == [1,3,5]
  end

  it "should skip next instruction and keep skipping if its also #" do
    @rbf.run('1#2#3#4#5678@')
    @rbf.stack.should == [1, 6, 7, 8]
  end

  it "should get value of program instruction" do
    @rbf.run('09g@<<<<<0')
    @rbf.stack.should == [48]
  end

  it "should put value of program instruction" do
    @rbf.run('0991+6*5+p@<<<<<0')
    @rbf.stack.should == []
    @rbf.code[0][9].chr.should == 'A'
  end

  it "should ask the user for a number" do
    redirect_stdin("0009") do
      @rbf.run('01234&@')
      @rbf.stack.should == [0, 1, 2, 3, 4, 9]
    end
  end

  it "should ask the user for a character" do
    redirect_stdin("ABCD") do
      @rbf.run('01234~@')
      @rbf.stack.should == [0, 1, 2, 3, 4, 65]
    end
  end

  it "should solve fizzbuzz" do
code = <<-EOS
55*4*v    _   v                                                                 )
v   <>:1-:^                                                                     )
    |:<$      <    ,*48 <                                                       )
    @>0"zzif">:#,_$      v                                                      )
>:3%!|    >0"zzub">:#,_$^                                                       )
     >:5%!|                                                                     )
v "buzz"0<>:.           ^                                                       )
         |!%5:           <                                                      )
>:#,_   $>              ^)
EOS
    result = redirect_stdout do
      @rbf.run(code)
    end

    result.should == "1 2 fizz 4 buzz fizz 7 8 fizz buzz 11 fizz 13 14 fizzbuzz " +
                     "16 17 fizz 19 buzz fizz 22 23 fizz buzz 26 fizz 28 29 fizzbuzz " +
                     "31 32 fizz 34 buzz fizz 37 38 fizz buzz 41 fizz 43 44 fizzbuzz " +
                     "46 47 fizz 49 buzz fizz 52 53 fizz buzz 56 fizz 58 59 fizzbuzz " +
                     "61 62 fizz 64 buzz fizz 67 68 fizz buzz 71 fizz 73 74 fizzbuzz 76 " +
                     "77 fizz 79 buzz fizz 82 83 fizz buzz 86 fizz 88 89 fizzbuzz 91 92 " +
                     "fizz 94 buzz fizz 97 98 fizz buzz "
  end

  it "should wrap around to the right" do
    @rbf.run <<-EOS
>>v
1@>>>
EOS
    @rbf.stack.should == [1]
  end

  it "should wrap around to the left" do
    @rbf.run <<-EOS
>>>>>>v
<<<<<<<    @1
EOS
    @rbf.stack.should == [1]
  end

  it "should wrap around at the bottom" do
    @rbf.run <<-EOS
v1
v@
>v
 v
 v
EOS
    @rbf.stack.should == [1]
  end

  it "should wrap around at the top" do
    @rbf.run <<-EOS
^
@
1
EOS
    @rbf.stack.should == [1]
  end

  it "should ask the user for a number when dividing by zero" do
    redirect_stdin '5' do
      @rbf.run('00/@')
      @rbf.stack.should == [5]
    end
  end

  it "should ask the user for a number when modulo dividing by zero" do
    redirect_stdin '5' do
      @rbf.run('00%@')
      @rbf.stack.should == [5]
    end
  end

  def redirect_stdout
    oldstdout, $stdout = $stdout, StringIO.new
    yield
    $stdout.string
  ensure
    $stdout = oldstdout
  end

  def redirect_stdin(str)
    oldstdin, $stdin = $stdin, StringIO.new(str)
    yield
  ensure
    $stdin = oldstdin
  end
end
