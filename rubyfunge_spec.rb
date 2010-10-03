require 'rubyfunge'
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


  def redirect_stdout
    oldstdout, $stdout = $stdout, StringIO.new
    yield
    $stdout.string
  ensure
    $stdout = oldstdout
  end
end
