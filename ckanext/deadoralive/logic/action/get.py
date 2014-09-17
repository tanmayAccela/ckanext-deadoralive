import datetime

import ckanext.deadoralive.model.results as results
import ckanext.deadoralive.config as config


def get_resources_to_check(context, data_dict):
    """Return a list of up to ``n`` resource IDs to be checked.

    Returns up to ``n`` resource IDs to be checked for broken links.

    Resources that have not been checked before will be returned first, oldest
    resources first.

    Resources that have not been checked in the last 24 hours (configurable:
    ``ckanext.deadoralive.recheck_resources_after``) will be returned next,
    most-recently-checked resources last.

    As soon as a resource's ID is returned by this function that resource is
    considered to have a "pending" check (we are expecting to receive a link
    check result for that resource soon). Resources with pending checks will
    not be returned by this function again for at least 2 hours (configurable:
    ``ckanext.deadoralive.resend_pending_resources_after``).

    :param n: the maximum number of resources to return at once
    :type n: int

    :rtype: list of strings

    """
    # TODO: Authorization.
    # TODO: Validation.

    recheck_resources_after = config.recheck_resources_after
    since_delta = datetime.timedelta(hours=recheck_resources_after)
    resend_pending_resources_after = (
        config.resend_pending_resources_after)
    pending_since_delta = datetime.timedelta(
        hours=resend_pending_resources_after)

    n = data_dict.get("n", 50)

    return results.get_resources_to_check(n, since=since_delta,
                                          pending_since=pending_since_delta)


def get(context, data_dict):
    """Get the latest link check result data for a resource.

    :param resource_id: the resource to return the result data for
    :type resource_id: string

    :returns: the latest link check data for the resource
    :rtype: dict

    """
    # TODO: Authorization.
    # TODO: Validation.
    resource_id = data_dict["resource_id"]
    result = results.get(resource_id)

    # datetimes aren't JSON serializable.
    result["last_checked"] = result["last_checked"].isoformat()
    if result["last_successful"]:
        result["last_successful"] = result["last_successful"].isoformat()
    if result["pending_since"]:
        result["pending_since"] = result["pending_since"].isoformat()

    return result
