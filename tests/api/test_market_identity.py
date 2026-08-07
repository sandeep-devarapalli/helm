import asyncio
from decimal import Decimal
from uuid import uuid4

import pytest
from helm.domain.models import (
    Currency,
    Instrument,
    InstrumentKind,
    Listing,
    ListingStatus,
    Venue,
    VenueKind,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


def test_structural_cross_market_fixtures_keep_symbols_venue_scoped(
    api_context,
) -> None:
    async def exercise() -> list[tuple[object, ...]]:
        async with api_context.session_factory() as session:
            usd = Currency(code="USD", name="US dollar", minor_unit=2)
            inr = Currency(code="INR", name="Indian rupee", minor_unit=2)
            xnas = Venue(
                code="XNAS",
                mic="XNAS",
                kind=VenueKind.SECURITIES_EXCHANGE.value,
                name="Nasdaq fixture venue",
                timezone="America/New_York",
            )
            alt_us = Venue(
                code="ALT_US",
                kind=VenueKind.SECURITIES_EXCHANGE.value,
                name="Alternate US fixture venue",
                timezone="America/New_York",
            )
            xnse = Venue(
                code="XNSE",
                mic="XNSE",
                kind=VenueKind.SECURITIES_EXCHANGE.value,
                name="NSE fixture venue",
                timezone="Asia/Kolkata",
            )
            coinbase = Venue(
                code="COINBASE",
                kind=VenueKind.CRYPTO_VENUE.value,
                name="Crypto fixture venue",
                timezone="UTC",
            )
            arcx = Venue(
                code="ARCX",
                mic="ARCX",
                kind=VenueKind.SECURITIES_EXCHANGE.value,
                name="NYSE Arca fixture venue",
                timezone="America/New_York",
            )
            apple = Instrument(kind=InstrumentKind.COMMON_STOCK.value, name="Apple fixture")
            reliance = Instrument(
                kind=InstrumentKind.COMMON_STOCK.value,
                name="Reliance fixture",
            )
            bitcoin = Instrument(
                kind=InstrumentKind.CRYPTO_ASSET.value,
                name="Bitcoin fixture",
            )
            gold_etf = Instrument(kind=InstrumentKind.ETF.value, name="Gold ETF fixture")
            session.add_all(
                [usd, inr, xnas, alt_us, xnse, coinbase, arcx, apple, reliance, bitcoin, gold_etf]
            )
            await session.flush()
            session.add_all(
                [
                    Listing(
                        instrument_id=apple.id,
                        venue_id=xnas.id,
                        venue_symbol="AAPL",
                        quote_currency_code="USD",
                        price_increment=Decimal("0.01"),
                        quantity_increment=Decimal("1"),
                    ),
                    Listing(
                        instrument_id=apple.id,
                        venue_id=alt_us.id,
                        venue_symbol="AAPL",
                        quote_currency_code="USD",
                        price_increment=Decimal("0.01"),
                        quantity_increment=Decimal("1"),
                    ),
                    Listing(
                        instrument_id=reliance.id,
                        venue_id=xnse.id,
                        venue_symbol="RELIANCE",
                        quote_currency_code="INR",
                        price_increment=Decimal("0.05"),
                        quantity_increment=Decimal("1"),
                    ),
                    Listing(
                        instrument_id=bitcoin.id,
                        venue_id=coinbase.id,
                        venue_symbol="BTC-USD",
                        quote_currency_code="USD",
                        price_increment=Decimal("0.01"),
                        quantity_increment=Decimal("0.00000001"),
                    ),
                    Listing(
                        instrument_id=gold_etf.id,
                        venue_id=arcx.id,
                        venue_symbol="GLD",
                        quote_currency_code="USD",
                        price_increment=Decimal("0.01"),
                        quantity_increment=Decimal("1"),
                    ),
                ]
            )
            await session.commit()

            return list(
                (
                    await session.execute(
                        select(
                            Venue.code,
                            Listing.venue_symbol,
                            Instrument.id,
                            Instrument.kind,
                            Listing.quote_currency_code,
                            Listing.price_increment,
                            Listing.quantity_increment,
                        )
                        .join(Listing, Listing.venue_id == Venue.id)
                        .join(Instrument, Instrument.id == Listing.instrument_id)
                        .order_by(Venue.code)
                    )
                ).all()
            )

    rows = asyncio.run(exercise())

    assert [(row[0], row[1], row[3], row[4]) for row in rows] == [
        ("ALT_US", "AAPL", "common_stock", "USD"),
        ("ARCX", "GLD", "etf", "USD"),
        ("COINBASE", "BTC-USD", "crypto_asset", "USD"),
        ("XNAS", "AAPL", "common_stock", "USD"),
        ("XNSE", "RELIANCE", "common_stock", "INR"),
    ]
    assert rows[0][2] == rows[3][2]
    assert all(isinstance(row[5], Decimal) and isinstance(row[6], Decimal) for row in rows)
    assert rows[2][6] == Decimal("0.000000010000000000")


def test_duplicate_symbol_on_one_venue_is_rejected(api_context) -> None:
    async def exercise() -> None:
        async with api_context.session_factory() as session:
            currency = Currency(code="USD", name="US dollar", minor_unit=2)
            venue = Venue(
                code="XNAS",
                mic="XNAS",
                kind=VenueKind.SECURITIES_EXCHANGE.value,
                name="Nasdaq fixture venue",
                timezone="America/New_York",
            )
            first = Instrument(kind=InstrumentKind.COMMON_STOCK.value, name="First")
            second = Instrument(kind=InstrumentKind.COMMON_STOCK.value, name="Second")
            session.add_all([currency, venue, first, second])
            await session.flush()
            session.add_all(
                [
                    Listing(
                        instrument_id=first.id,
                        venue_id=venue.id,
                        venue_symbol="SAME",
                        quote_currency_code="USD",
                        price_increment=Decimal("0.01"),
                        quantity_increment=Decimal("1"),
                    ),
                    Listing(
                        instrument_id=second.id,
                        venue_id=venue.id,
                        venue_symbol="SAME",
                        quote_currency_code="USD",
                        price_increment=Decimal("0.01"),
                        quantity_increment=Decimal("1"),
                    ),
                ]
            )
            with pytest.raises(IntegrityError):
                await session.commit()

    asyncio.run(exercise())


def test_whitespace_cannot_bypass_same_venue_symbol_uniqueness(api_context) -> None:
    async def exercise() -> None:
        async with api_context.session_factory() as session:
            currency = Currency(code="USD", name="US dollar", minor_unit=2)
            venue = Venue(
                code="XNAS",
                mic="XNAS",
                kind=VenueKind.SECURITIES_EXCHANGE.value,
                name="Nasdaq fixture venue",
                timezone="America/New_York",
            )
            first = Instrument(kind=InstrumentKind.COMMON_STOCK.value, name="First")
            second = Instrument(kind=InstrumentKind.COMMON_STOCK.value, name="Second")
            session.add_all([currency, venue, first, second])
            await session.flush()
            session.add_all(
                [
                    Listing(
                        instrument_id=first.id,
                        venue_id=venue.id,
                        venue_symbol="SAME",
                        quote_currency_code="USD",
                        price_increment=Decimal("0.01"),
                        quantity_increment=Decimal("1"),
                    ),
                    Listing(
                        instrument_id=second.id,
                        venue_id=venue.id,
                        venue_symbol=" SAME ",
                        quote_currency_code="USD",
                        price_increment=Decimal("0.01"),
                        quantity_increment=Decimal("1"),
                    ),
                ]
            )
            with pytest.raises(IntegrityError):
                await session.commit()

    asyncio.run(exercise())


@pytest.mark.parametrize(
    ("model"),
    [
        Currency(code="usd", name="Lowercase code", minor_unit=2),
        Venue(
            code="BAD",
            kind="broker",
            name="Invalid venue kind",
            timezone="UTC",
        ),
        Instrument(kind="future", name="Deferred derivative"),
    ],
)
def test_invalid_identity_classifications_fail_closed(
    api_context,
    model: object,
) -> None:
    async def exercise() -> None:
        async with api_context.session_factory() as session:
            session.add(model)
            with pytest.raises(IntegrityError):
                await session.commit()

    asyncio.run(exercise())


@pytest.mark.parametrize(
    ("price_increment", "quantity_increment", "status"),
    [
        (Decimal("0"), Decimal("1"), ListingStatus.ACTIVE.value),
        (Decimal("0.01"), Decimal("0"), ListingStatus.ACTIVE.value),
        (Decimal("-0.01"), Decimal("1"), ListingStatus.ACTIVE.value),
        (Decimal("0.01"), Decimal("-1"), ListingStatus.ACTIVE.value),
        (Decimal("0.01"), Decimal("1"), "halted"),
    ],
)
def test_invalid_listing_shapes_are_rejected(
    api_context,
    price_increment: Decimal,
    quantity_increment: Decimal,
    status: str,
) -> None:
    async def exercise() -> None:
        async with api_context.session_factory() as session:
            currency = Currency(code="USD", name="US dollar", minor_unit=2)
            venue = Venue(
                code="XNAS",
                mic="XNAS",
                kind=VenueKind.SECURITIES_EXCHANGE.value,
                name="Nasdaq fixture venue",
                timezone="America/New_York",
            )
            instrument = Instrument(kind=InstrumentKind.COMMON_STOCK.value, name="Fixture")
            session.add_all([currency, venue, instrument])
            await session.flush()
            session.add(
                Listing(
                    instrument_id=instrument.id,
                    venue_id=venue.id,
                    venue_symbol="FAIL",
                    quote_currency_code="USD",
                    price_increment=price_increment,
                    quantity_increment=quantity_increment,
                    status=status,
                )
            )
            with pytest.raises(IntegrityError):
                await session.commit()

    asyncio.run(exercise())


def test_unknown_market_identity_references_are_rejected(
    api_context,
) -> None:
    async def exercise() -> None:
        async with api_context.session_factory() as session:
            session.add(
                Listing(
                    instrument_id=uuid4(),
                    venue_id=uuid4(),
                    venue_symbol="UNKNOWN",
                    quote_currency_code="USD",
                    price_increment=Decimal("0.01"),
                    quantity_increment=Decimal("1"),
                )
            )
            with pytest.raises(IntegrityError):
                await session.commit()

    asyncio.run(exercise())
