# The point of this file is to create a small test_harness on a random sample of the data
# We take 5 music and 5 non-music examples, and see where this takes us

from ..utilities.data_processing import get_five_of_each

print(get_five_of_each())