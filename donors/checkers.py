from .models import Donor
from datetime import date

def check_donation_date(pk: int) -> int:
    """
    Checks the last day of donation and returns the number of days since donation.
    
    Params:
        - pk (int): Donor's ID
    
    Returns:
        - int: Number of days since the last donation.
    """
    donor = Donor.objects.get(pk=pk)
    days_since_last_donation = (date.today() - donor.last_donation_date).days
    return days_since_last_donation

def check_donors_weight(pk: int) -> int:
    """
    Returns Donor's current weight.
    
    Params:
        - pk (int): Donor's ID
    
    Returns:
        - int: Donor's weight in kilograms.
    """
    donor = Donor.objects.get(pk=pk)
    weight = donor.weight_kg
    return weight

def is_donor_eligible_to_donate(donor_pk: int) -> bool:
    """
    Determines if the donor is eligible to donate based on their last donation date, weight, and number of donations.
    
    Params:
        - donor_pk (int): Donor's ID
    
    Returns:
        - bool: True if the donor is eligible to donate, False otherwise.
    """
    donor = Donor.objects.get(pk=donor_pk)
    
    last_donation_date = check_donation_date(donor_pk)
    weight = check_donors_weight(donor_pk)
    no_of_donation = donor.get_no_of_donations

    if last_donation_date > 10 and weight > 70 and no_of_donation <= 10:    
        return True
    else: 
        return False
