/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   2_parse_main.c                                    :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:39 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	process_input(t_program *program)
{
	if (parse_options(program) == ERROR)
		return (ERROR);
	if (parse_numbers_into_stack_a(program) == ERROR)
		return (ERROR);
	return (SUCCESS);
}

int	parse_options(t_program *program)
{
	int	i;

	i = 1;
	while (i < program->argc)
	{
		if (is_option(program->argv[i]))
		{
			if (parse_one_option(program, program->argv[i]) == ERROR)
				return (ERROR);
		}
		i++;
	}
	if (program->requested_strategy == STRATEGY_NONE)
		program->requested_strategy = STRATEGY_ADAPTIVE;
	return (SUCCESS);
}

int	is_strategy_option(const char *argument)
{
	if (strings_are_equal(argument, "--simple"))
		return (1);
	if (strings_are_equal(argument, "--medium"))
		return (1);
	if (strings_are_equal(argument, "--complex"))
		return (1);
	if (strings_are_equal(argument, "--adaptive"))
		return (1);
	if (strings_are_equal(argument, "--ultra"))
		return (1);
	return (0);
}

t_strategy	get_strategy_from_option(const char *argument)
{
	if (strings_are_equal(argument, "--simple"))
		return (STRATEGY_SIMPLE);
	if (strings_are_equal(argument, "--medium"))
		return (STRATEGY_MEDIUM);
	if (strings_are_equal(argument, "--complex"))
		return (STRATEGY_COMPLEX);
	if (strings_are_equal(argument, "--adaptive"))
		return (STRATEGY_ADAPTIVE);
	if (strings_are_equal(argument, "--ultra"))
		return (STRATEGY_ULTRA);
	return (STRATEGY_NONE);
}

int	parse_one_option(t_program *program, const char *argument)
{
	t_strategy	strategy;

	if (strings_are_equal(argument, "--bench"))
		return (program->bench_enabled = 1, SUCCESS);
	if (strings_are_equal(argument, "--debug"))
		return (program->debug_enabled = 1, SUCCESS);
	if (!is_strategy_option(argument))
		return (ERROR);
	strategy = get_strategy_from_option(argument);
	if (program->requested_strategy != STRATEGY_NONE
		&& program->requested_strategy != strategy)
		return (ERROR);
	program->requested_strategy = strategy;
	return (SUCCESS);
}
