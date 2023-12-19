from app.models.donats_in_projs import DonatsInProjs


def def_invested(target, sources):
    objects = []
    if not sources:
        objects.append(target)
        return objects

    for source in sources:
        source_nead, target_balance = (
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        if target_balance > source_nead:
            source.invested()
            target.invested_amount += source_nead
            donate = DonatsInProjs()
            donate.create(
                target.__class__.__name__,
                target.id,
                source.id,
                source_nead
            )
            objects.extend((donate, source))
        elif target_balance < source_nead:
            source.invested_amount += target_balance
            target.invested()
            donate = DonatsInProjs()
            donate.create(
                target.__class__.__name__,
                target.id,
                source.id,
                target_balance
            )
            objects.extend((target, source, donate))
            return objects
        elif target_balance == source_nead:
            source.invested()
            target.invested()
            donate = DonatsInProjs()
            donate.create(
                target.__class__.__name__,
                target.id,
                source.id,
                source_nead
            )
            objects.extend((target, source, donate))
            return objects

    if target not in objects:
        objects.append(target)
        return objects
