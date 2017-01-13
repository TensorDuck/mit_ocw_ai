from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    #print "for hypothesis : %s" % hypothesis
    possible_rules = []
    for zrules in rules:
        if match(zrules.consequent()[0], hypothesis):
            possible_rules.append(zrules)
        else:
            if match(zrules.consequent()[0], hypothesis) is None:
                pass
            else:
                possible_rules.append(zrules)

    if len(possible_rules) == 0:
        # no rules match this
        return hypothesis
    else:
        # some other rules match, encapsulate OR statement with an AND statement
        or_all = OR(hypothesis)
        for idx, zrules in enumerate(possible_rules):
            binding_list = match(zrules.consequent()[0], hypothesis)
            if not isinstance(zrules.antecedent(), list):
                iterate_over_antecedents = [zrules.antecedent()]
            else:
                iterate_over_antecedents = zrules.antecedent()
            if isinstance(zrules.antecedent(), OR):
                for jdx, ant in enumerate(iterate_over_antecedents):
                    add_this_or = backchain_to_goal_tree(rules, populate(ant, binding_list))
                    if jdx == 0:
                        this_or_all = OR(add_this_or)
                    else:
                        this_or_all = OR(this_or_all, add_this_or)
                this_or_all = simplify(this_or_all)
                or_all = OR(or_all, this_or_all)
            else:
                for jdx, ant in enumerate(iterate_over_antecedents):
                    add_this_and = backchain_to_goal_tree(rules, populate(ant, binding_list))
                    if jdx == 0:
                        and_all = AND(add_this_and)
                    else:
                        and_all = AND(and_all, add_this_and)
                and_all = simplify(and_all)
                or_all = OR(or_all, and_all)

        return simplify(or_all)


    raise NotImplementedError

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
