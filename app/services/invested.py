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
            objects.append(source)
        elif target_balance < source_nead:
            source.invested_amount += target_balance
            target.invested()
            objects.extend((target, source))
            return objects
        elif target_balance == source_nead:
            source.invested()
            target.invested()
            objects.extend((target, source))
            return objects

    if target not in objects:
        objects.append(target)
        return objects
