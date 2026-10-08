Feature: Booking a movie seat
  Background:
    Given a movie "Dune" with seats "A1" and "A2"
    And I am logged in as "alice"

  Scenario: Booking an available seat
    When I book seat "A1" for "Dune"
    Then I see "Seat booked for Dune!"
    And seat "A1" is no longer offered for "Dune"

  Scenario: A seat that is already taken cannot be booked again
    Given I have booked seat "A1" for "Dune"
    When I book seat "A1" for "Dune"
    Then I see "already taken"