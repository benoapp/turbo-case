# TDD: Test Driven Development
1. Typical development flow has looooooong feedback loop
2. TDD by example:
	1. Card Formatter
```python
def helper()
	pass
@Test
def test_card_formatter(): ✅
	# Arrange 
	input = "5555444444444444"
	# Act
	actual = format_credit_card(input)
	# Assert
	assert actual == "5555 4444 4444 4444"

@Test
def test_card_formatter_more_than16(): ✅
	# Given
	input = "555544444444444433"
	# When
	actual = format_credit_card(input)
	# Then
	assert actual == "5555 4444 4444 4444 33
	
def format_credit_card(unformatted_credit_card):
	# regext formatter
	return rex_format(unformatted_credit_card, '{{insert regext}}')
#	for i in Range(16):
#		if(i % 4)
#			formatted_credit_card
#			# split at index
#			unformatted_credit_card.split(..)
#			# add a white space
#			# rejoin
#			return formatted_credit_card
#			
```
3. Flow
	1. ❌: undefined -> ❌: assertion failure -> ✅ Test pass -> ✅ Refactor
4. Mini doors to your code block
# BDD:  Behavior Driven Development
1. Gherkin
	1. Feature, Scenario, Given, When, Then, But, And
	2. Scenario Outline, Background, * 
```gherkin
Feature:
	As a Student, I want to know if I am in the deans list, so that I can tell my familiy

	Scenario: Student semester GPA is 4.5, but compulative is 4.0
		Given student comulative GPA is 4.0 
		When student scores 4.5 in current semester
		Then student should receive congratualationss email
		And student should receive 5% schoolarship
		
	Scenario: Student comulative GPA is 4.5, but not this semeseter
		When last professor clicks on submit button
		And dean click on publish grades button
		And all students grades are ready
		And dean click on yes for "Are you sure"  
		
	Scenario: Student arithmatic GPA is 4.4999999
		# TODO
```
2. A good BDD doen't have tech details
3. Automation path
```python
# Student semester GPA is 4.5, but compulative is 4.0
@Test
def semester3point5():
	student = {
		accGPA: 3.0,
		currentGPA: 3.5, 
		schoolshipPercentage:0 
	}

	actual = makeDeansList(student)

	assert actual.isDeansList
	assert actual.schoolarShip = 5.0	

def isDeansList(student):
	return  student.currentGPA >= 3.5
```
3. manual test docs
```yaml
Precondition: # Given
- Student is not in deans list
Steps: # When
- Dean publishes grades
Expect: # Then
- Student opens student portal
- Navigate to financial page
- Student should see 5%
```
4. 
```d2
bdd: |feature
Feature: partial payments
  Scenario: Even
    When checkout 10
    Then pay 5 now
    And pay 5 later
|

js: |javascript
When("checkout 10") {
// click on split payment
CheckoutPage.clickSplitPayment()

// fill credit card
CheckoutPage.fillCard(DEFAULT_CARD)

// fill name

// click on pay
}

Then("pay 5 now") { /**/ }

And("pay 5 later") { /**/ }
|

js-mid: |javascript
function fillCard(card) {
cssLocator = "#checkoutform #input[nam=card]"
}
|

manual: |yaml
precondition:
- checkout a deal
steps:
- click on split payment
- fill default credit card
- click on pay
result:
- success
|

bdd -> js -> js-mid
bdd -> manual: ??
js -> testiny: mark as automated
bdd -> git: git push
js -> git: git push
git -> testiny: ci/cd scripts
manual -> git: git push
```
