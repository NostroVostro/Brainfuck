# helloworld.bf
# I'm really back at Brainfuck, but
# given some time, and practice, 
# I could probably make this a lot shorter

# H
>> ++++ [
	< ++++ ++++ ++++ ++++ ++
	> -
]<

# e
>> ++++ [
	< +++++ +++++ +++++ +++++ +++++
	> - 
]<+ 

# l
>> ++ ++[
	< +++++ +++++ +++++ +++++ +++++ ++
	> -
]< 

# l
>> ++ ++[
	< +++++ +++++ +++++ +++++ +++++ ++
	> -
]< 

# o
>> ++ + ++[
	< +++++ +++++ +++++ +++++ ++
	> -
]<+

# (space)
>> ++++ [
	< ++++ ++++
	> -
]<

# W
>> ++++ [
	< +++++ +++++ +++++ +++++ +
	> -
]<+++

# o
>> ++ + ++[
	< +++++ +++++ +++++ +++++ ++
	> -
]<+

# r
>> ++ + ++[
	< +++++ +++++ +++++ +++++ ++
	> -
]<++++

# l
>> ++ ++[
	< +++++ +++++ +++++ +++++ +++++ ++
	> -
]< 

# d
>> ++++ [
	< +++++ +++++ +++++ +++++ +++++
	> - 
]<

# (exclamation point)
>> ++++ [
	< ++++ ++++
	> -
]<+

# Removes ending zero
# and takes us back to the 
# first cell which is 0
>!<[<]!

# Takes us back over the
# cells and prints them
[.>]!