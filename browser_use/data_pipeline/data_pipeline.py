from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field


class CabinInformation(BaseModel):
    cabin_number: str
    cabin_type: str
    cabin_category: str

class PassengerInformation(BaseModel):
    passenger_name: str
    passenger_email: str

class PassengerDetail(BaseModel):
    selling_price: Optional[float] = Field(None, alias="sellingPrice")
    seaware_stage_type: str = Field(alias="seawareStageType")
    passenger_stage_id: Optional[int] = Field(None, alias="passengerStageId")
    passenger_id: Optional[int] = Field(None, alias="passengerId")
    is_cancelled: Optional[bool] = Field(None, alias="isCancelled")
    cost: Optional[float] = None

class Passenger(BaseModel):
    seaware_guest_type: str = Field(alias="seawareGuestType")
    passenger_id: int = Field(alias="passengerId")
    name: str
    medical_form_status: str = Field(alias="medicalFormStatus")
    is_lead: bool = Field(alias="isLead")
    is_cancelled: bool = Field(alias="isCancelled")
    email: str
    date_of_birth: datetime = Field(alias="dateOfBirth")
    customer_id: int = Field(alias="customerId")
    cancellation_date: Optional[datetime] = Field(None, alias="cancellationDate")

class Cabin(BaseModel):
    passenger_details: List[PassengerDetail] = Field(alias="passengerDetails")
    mask: Optional[int] = None
    index: Optional[int] = None
    category: str
    cabin_number: str = Field(alias="cabinNumber")

class Promotion(BaseModel):
    passenger_stage_id: Optional[int] = Field(None, alias="passengerStageId")
    passenger_id: Optional[int] = Field(None, alias="passengerId")
    code: str

class AddOn(BaseModel):
    supplier: Optional[str] = None
    status: str
    start_date_time: datetime = Field(alias="startDateTime")
    selling_price: float = Field(alias="sellingPrice")
    seaware_reservation_id: int = Field(alias="seawareReservationId")
    quantity: int
    passenger_details: List[PassengerDetail] = Field(alias="passengerDetails")
    notes: Optional[str] = None
    mandatory: bool
    end_date_time: datetime = Field(alias="endDateTime")
    description: str
    confirmation_number: str = Field(alias="confirmationNumber")
    code: str
    booking_stage_id: int = Field(alias="bookingStageId")

class Sailing(BaseModel):
    travel_type: str = Field(alias="travelType")
    to_port: str = Field(alias="toPort")
    supplier: Optional[str] = None
    status: str
    start_date_time: datetime = Field(alias="startDateTime")
    ship_rooms: List[Any] = Field(alias="shipRooms")
    ship_name: str = Field(alias="shipName")
    ship_comments: str = Field(alias="shipComments")
    ship_code: str = Field(alias="shipCode")
    selling_price: float = Field(alias="sellingPrice")
    seaware_reservation_id: int = Field(alias="seawareReservationId")
    seaware_package_id: int = Field(alias="seawarePackageId")
    sailing_type: Optional[str] = Field(None, alias="sailingType")
    sail_id: str = Field(alias="sailId")
    sail_code: str = Field(alias="sailCode")
    promotions: List[Promotion]
    product_type_id: int = Field(alias="productTypeId")
    package_code: str = Field(alias="packageCode")
    number_of_vehicles: int = Field(alias="numberOfVehicles")
    notes: Optional[str] = None
    is_via_kirkenes: bool = Field(alias="isViaKirkenes")
    is_in_seaware_repair_queue: bool = Field(alias="isInSeawareRepairQueue")
    from_port: str = Field(alias="fromPort")
    excursions: List[Any]
    end_date_time: datetime = Field(alias="endDateTime")
    destination: str
    description: str
    cruise_nights: float = Field(alias="cruiseNights")
    confirmation_number: str = Field(alias="confirmationNumber")
    closed_promotion: str = Field(alias="closedPromotion")
    cabins: List[Cabin]
    booking_stage_voyage_seaware_id: int = Field(alias="bookingStageVoyageSeawareId")
    booking_stage_id: int = Field(alias="bookingStageId")
    add_ons: List[AddOn] = Field(alias="addOns")

class PassengerGroup(BaseModel):
    tickets_sent_by_post: bool = Field(alias="ticketsSentByPost")
    tickets_sent_by_email: bool = Field(alias="ticketsSentByEmail")
    send_records_by: Optional[str] = Field(None, alias="sendRecordsBy")
    sailings: List[Sailing]
    promotions: List[Promotion]
    paying_customer_id: Optional[int] = Field(None, alias="payingCustomerId")
    passengers: List[Passenger]
    passenger_group_id: int = Field(alias="passengerGroupId")
    packages: List[Any]  # You could define a Package model if needed
    name: str
    is_cancelled: bool = Field(alias="isCancelled")
    flights: List[Any]  # You could define a Flight model if needed
    financial_overview: Dict[str, float] = Field(alias="financialOverview")
    cancellations: List[Any]
    cancellation_reason: Optional[str] = Field(None, alias="cancellationReason")
    cancellation_date_time: Optional[datetime] = Field(None, alias="cancellationDateTime")

class Agency(BaseModel):
    phone: str
    name: str
    invoice_type: str = Field(alias="invoiceType")
    email: str
    contact_id: int = Field(alias="contactId")
    agency_id: int = Field(alias="agencyId")

class Reservation(BaseModel):
    tour: str
    status: str
    start_date_time: datetime = Field(alias="startDateTime")
    secondary_booking_source: Optional[str] = Field(None, alias="secondaryBookingSource")
    payments: List[Any]
    pay_later: bool = Field(alias="payLater")
    passenger_groups: List[PassengerGroup] = Field(alias="passengerGroups")
    notes: Optional[str] = None
    modified_by: str = Field(alias="modifiedBy")
    marketing_source: str = Field(alias="marketingSource")
    market: str
    is_platinum: bool = Field(alias="isPlatinum")
    invoices: List[Any]
    group_booking: Optional[Any] = Field(None, alias="groupBooking")
    financial_overview: Dict[str, float] = Field(alias="financialOverview")
    final_due_date: datetime = Field(alias="finalDueDate")
    end_date_time: datetime = Field(alias="endDateTime")
    deposit_due_date: datetime = Field(alias="depositDueDate")
    departure_date_time: datetime = Field(alias="departureDateTime")
    created_date_time: datetime = Field(alias="createdDateTime")
    created_by: str = Field(alias="createdBy")
    company: str
    cancellation_reason: Optional[str] = Field(None, alias="cancellationReason")
    cancellation_date_time: Optional[datetime] = Field(None, alias="cancellationDateTime")
    can_auto_cancel: bool = Field(alias="canAutoCancel")
    brochure: str
    booking_source: str = Field(alias="bookingSource")
    booking_sfid: str = Field(alias="bookingSFID")
    booking_id: int = Field(alias="bookingId")
    booking_currency: str = Field(alias="bookingCurrency")
    booking_area: str = Field(alias="bookingArea")
    agency: Agency

    class Config:
        populate_by_name = True

class DataPipeline:
    def __init__(self, reservation_data: dict):
        # Set up Jinja environment
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template("reservation_prompt.j2")
        self.reservation_data = Reservation.model_validate(reservation_data)

    def create_prompt_from_reservation_data(self) -> str:
        """Create a prompt from reservation data."""
        # Parse the reservation data into a Pydantic model
        
        start_date = self.extract_start_date_from_reservation_data()
        cabin_information_list = self.extract_cabin_information_from_reservation_data()
        passenger_information = self.extract_passenger_information_from_reservation_data()

        # Render the template with the data
        prompt = self.template.render(
            start_date=start_date,
            cabins=cabin_information_list,
            passengers=passenger_information
        )
        
        return prompt
    
    def extract_start_date_from_reservation_data(self) -> datetime:
        """Extract the start date from the reservation data."""
        return self.reservation_data.start_date_time
    
    def _get_unique_cabins(self, cabins: list[Cabin]) -> list[Cabin]:
        """Get the unique cabins from the reservation data based on category and cabin number."""
        unique_cabins = []
        seen = set()
        
        for cabin in cabins:
            # Create a unique key based on category and cabin number
            key = (cabin.category, cabin.cabin_number)
            
            # Only add if we haven't seen this combination before
            if key not in seen:
                seen.add(key)
                unique_cabins.append(cabin)
                
        return unique_cabins
    
    def extract_cabin_information_from_reservation_data(self) -> list[CabinInformation]:
        """Extract the cabin information from the reservation data."""
        passenger_group = self.reservation_data.passenger_groups[0]
        sailing = passenger_group.sailings[0]
        unique_cabins = self._get_unique_cabins(sailing.cabins)

        return [CabinInformation(
            cabin_number=cabin.cabin_number,
            cabin_type=cabin.passenger_details[0].seaware_stage_type if cabin.passenger_details else "Unknown",
            cabin_category=cabin.category,
        ) for cabin in unique_cabins]
    

    def extract_passenger_information_from_reservation_data(self) -> list[PassengerInformation]:
        """Extract the passenger information from the reservation data."""
        passenger_group = self.reservation_data.passenger_groups[0]
        return [PassengerInformation(
            passenger_name=passenger.name,
            passenger_email=passenger.email,
        ) for passenger in passenger_group.passengers]