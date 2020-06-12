### py-pass-gen

--------------------------------------------------------------------------------

This program was inspired by Arnold G. Reinhold's DICEWARE technology. It
generates memorable, secure passphrases. While less secure than its analog
inspiration, it should work for the moderately paranoid. py-pass-gen utilizes
Python's SystemRandom class, a cryptographically secure pseudo-random
number generator.

For more memorable passwords that are still secure, use only one capital letter,
number and special character, but use at least 5 terms.

The overwrite menu option causes randomly inserted numbers, letters and
characters to be placed over the letter in the index they are assigned.

The display steps menu option is used for debugging and looking at how a
password was created, step by step. This can make it easier to understand and
remember later.

Any dictionary file can be used as long has it has one word per line with no
leading or trailing text. Words 7 characters or less are recommended. Just
replace dict.txt. The stock dictionary uses the medium and long word lists from
the most common 10000 English words in Google's Trillion Word Corpus. These
lists are available at https://github.com/first20hours/google-10000-english.

The entropy calculator can be used to determine the entropy of an existing
password.

The special characters used by the program are:
<div>
  <p>
    "~#%+-*^=@/\|<>()`&_!?.,:;'.
    <br>
  </p>
</div>

Any other characters will not be checked for by the entropy calculator, nor put
into generated passwords.

Remember: It does not matter how secure you make a password, it can still
readily be beaten out of you with a wrench.
