# TODO: turn into a library
from copy import deepcopy

downtime_duration = 10

class DefensiveSkill:
    def __init__(self, name, duration, cooldown, protection):
        self.name = name
        self.duration = duration
        self.cooldown = cooldown
        self.protection = protection # TODO: Protection attribute is added in case there are multiple full uptime rotations, in order to determine best defensive value
        self.current_cooldown = 0

def chain_subsequent_skills_recursively(skill_chains, skill_chain_pointer, rotation_duration, defensives_uptime, skill_pointers, include_downtime = False):
    skills = []
    for skill_pointer in skill_pointers:
        skills.append(deepcopy(skill_pointer))
    skill_chain = deepcopy(skill_chain_pointer)
    

    loop_counter = 0
    for skill in skills:
        if skill.current_cooldown <= 0:
            loop_counter += 1
            skill_chain.append(skill.name)
            
            skill.current_cooldown = skill.cooldown
            rotation_duration += skill.duration
            defensives_uptime += skill.duration
            for s in skills:
                s.current_cooldown -= skill.duration # cooldowns of all skills are adequately reduced after skill's duration has passed and we check for the next skill to use

            if rotation_duration < 400:
                chain_subsequent_skills_recursively(skill_chains, skill_chain, rotation_duration, defensives_uptime, skills, include_downtime)
            else:
                skill_chain.append(rotation_duration)
                skill_chain.append(defensives_uptime)
                skill_chains.append(skill_chain)
                return
    if loop_counter == 0:
        if include_downtime:
            skill_chain.append("downtime")
            rotation_duration += downtime_duration
            for s in skills:
                s.current_cooldown -= downtime_duration
            chain_subsequent_skills_recursively(skill_chains, skill_chain, rotation_duration, defensives_uptime, skills, include_downtime)
        else:
            skill_chain.append(rotation_duration)
            skill_chain.append(defensives_uptime)
            skill_chains.append(skill_chain)
    return
        
def convert_sublists_to_tuples(seq):
    return [tuple(x) for x in seq]

def remove_duplicates_from_list(seq):
    clean_seq = []
    for element in seq:
        if element not in clean_seq:
            clean_seq.append(element)
    return clean_seq


if __name__ == '__main__':
    rotation_duration = 0
    defensives_uptime = 0
    

    reprisal = DefensiveSkill('reprisal', 10, 60, 10) # TODO: optimize sequences for skills with the same cooldown, treating them as basically duplicates before considering protection value
    rampart = DefensiveSkill('rampart', 20, 90, 20)
    sentinel = DefensiveSkill('sentinel', 15, 120, 30)
    bulwark = DefensiveSkill('bulwark', 10, 90, 18) #protection value is approximation from forums, 18-20
    
    skill_pointers = (reprisal, rampart, sentinel, bulwark)

    skill_chains = []
    skill_chain = [] #list of every skill, ends with rotation_duration and defensive_uptime
    
    chain_subsequent_skills_recursively(skill_chains, skill_chain, rotation_duration, defensives_uptime, skill_pointers, True)

    skill_chains = convert_sublists_to_tuples(skill_chains)
    skill_chains = list(dict.fromkeys(skill_chains)) # remove duplicates while maintaining order
    longest_uptime = 0
    
    for chain in skill_chains:
        if chain[-1] > longest_uptime:
            longest_uptime = chain[-1]
        elif chain[-1] < longest_uptime:
            del chain

    longest_uptime_chains = []
    for chain in skill_chains:
        if chain[-1] == longest_uptime:
            longest_uptime_chains.append(chain)
    

