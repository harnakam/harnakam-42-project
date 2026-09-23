/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   6_benchmark.c                                     :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:33 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	print_benchmark_if_enabled(const t_program *program)
{
	if (!program->bench_enabled)
		return ;
	ft_putendl_fd("=== push_swap benchmark ===", 2);
	print_disorder(program->initial_disorder);
	ft_putstr_fd("Strategy: ", 2);
	ft_putendl_fd((char *) get_strategy_name(program->selected_strategy), 2);
	ft_putstr_fd("Complexity: ", 2);
	ft_putendl_fd((char *) get_strategy_complexity(
			program->selected_strategy), 2);
	print_operation_counts(&program->operations);
}

const char	*get_strategy_name(t_strategy strategy)
{
	if (strategy == STRATEGY_SIMPLE)
		return ("Spin Bubble Sort");
	if (strategy == STRATEGY_MEDIUM)
		return ("Spin Run Insertion");
	if (strategy == STRATEGY_COMPLEX)
		return ("Radix Sort");
	if (strategy == STRATEGY_ULTRA)
		return ("OptiCSRI");
	return ("Unknown");
}

const char	*get_strategy_complexity(t_strategy strategy)
{
	if (strategy == STRATEGY_SIMPLE)
		return ("O(n^2)");
	if (strategy == STRATEGY_MEDIUM)
		return ("O(n sqrt(n))");
	if (strategy == STRATEGY_COMPLEX)
		return ("O(n log(n))");
	if (strategy == STRATEGY_ULTRA)
		return ("operation optimized");
	return ("unknown");
}

void	print_disorder(double disorder)
{
	int	percentage;
	int	decimal;

	percentage = (int)(disorder * 100.0);
	decimal = (int)(disorder * 10000.0) % 100;
	ft_putstr_fd("Initial disorder: ", 2);
	ft_putnbr_fd(percentage, 2);
	ft_putchar_fd('.', 2);
	if (decimal < 10)
		ft_putchar_fd('0', 2);
	ft_putnbr_fd(decimal, 2);
	ft_putendl_fd("%", 2);
}

void	print_operation_counts(const t_operation_count *operations)
{
	print_size_line("Total operations: ", operations->total);
	print_size_line("sa:  ", operations->sa);
	print_size_line("sb:  ", operations->sb);
	print_size_line("ss:  ", operations->ss);
	print_size_line("pa:  ", operations->pa);
	print_size_line("pb:  ", operations->pb);
	print_size_line("ra:  ", operations->ra);
	print_size_line("rb:  ", operations->rb);
	print_size_line("rr:  ", operations->rr);
	print_size_line("rra: ", operations->rra);
	print_size_line("rrb: ", operations->rrb);
	print_size_line("rrr: ", operations->rrr);
}
