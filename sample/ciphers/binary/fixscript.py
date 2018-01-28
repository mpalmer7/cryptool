
s = "BABAAAABBBABAAABAABAAABAAAABBBABBABBAABBBAAABAABAA"
new = s.replace("B","0")
new = new.replace("A","1")

new2 = s.replace("A","0")
new2 = new2.replace("B","1")

print(new)
print(new2)